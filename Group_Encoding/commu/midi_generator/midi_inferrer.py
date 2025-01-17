import math
from typing import Tuple, List

import numpy as np
import torch
import torch.nn.functional as F
import yacs.config

from logger import logger
from commu.midi_generator.container import TransXlInputData
from commu.model.model import MemTransformerLM
from commu.preprocessor.encoder import TOKEN_OFFSET
from commu.preprocessor.utils.constants import DEFAULT_POSITION_RESOLUTION


class TeacherForceTask:
    def __init__(self, input_data):
        self.input_data = input_data
        self.next_tokens_forced = []
        self.no_sequence_appended = False
        self.is_incomplete = input_data.num_measures % 4 != 0
        self.incomplete_filled = not self.is_incomplete

        self.chord_token, self.chord_position = input_data.chord_token_components.values()
        assert len(self.chord_token) == len(self.chord_position), "Wrong Chord Length"
        self.chord_length = len(self.chord_token)
        self.inter_chord_flags = []
        for i in self.chord_position:
            if i == TOKEN_OFFSET.POSITION.value:
                self.inter_chord_flags.append(False)
            else:
                self.inter_chord_flags.append(True)

    def check_first_position(self, seq):
        """
        check if it's a token following a bar token
        """
        return self.incomplete_filled and seq[-1] == TOKEN_OFFSET.BAR.value

    def check_remnant_chord(self):
        """
        check if there any more chords to write
        if not, return False
        """
        return bool(len(self.chord_token) * len(self.chord_position))

    def check_length_fit(self):
        """
        check if one chord per bar needed
        """
        return self.chord_length == int(self.input_data.num_measures // 4 * 4)

    def check_position_fit(self, seq):
        """
        check if a chord token needs to be filled next
        """
        return seq[-2] == TOKEN_OFFSET.BAR.value and seq[-1] == TOKEN_OFFSET.POSITION.value

    # def check_one_chord_per_bar_case(self, seq):
    #     """
    #     case: one chord per bar
    #     """
    #     return (
    #         self.check_remnant_chord()
    #         and self.incomplete_filled
    #         and self.check_length_fit()
    #         and self.check_position_fit(seq)
    #     )

    # def check_mul_chord_per_bar_case(self, seq):
    #     """
    #     case: multiple chords per bar
    #     """
    #     is_first_position_chord = (
    #         self.check_remnant_chord()
    #         and self.incomplete_filled
    #         and not self.check_length_fit()
    #         and self.check_position_fit(seq)
    #     )

    #     is_inter_position_chord = (
    #         self.check_remnant_chord()
    #         and self.incomplete_filled
    #         and not self.check_length_fit()
    #         and not self.check_position_fit(seq)
    #         and seq[-1] == self.chord_position[0]
    #         and self.inter_chord_flags[0]
    #     )
    #     return is_first_position_chord or is_inter_position_chord

    def check_chord_position_passed(self, token):
        """
        in case a generated token skipped necessary position
        """
        if not self.check_remnant_chord():
            return False
        is_position_passed = (
            self.chord_position[0] < token < TOKEN_OFFSET.POSITION.value + DEFAULT_POSITION_RESOLUTION
            or token == TOKEN_OFFSET.BAR.value
        )
        return self.inter_chord_flags[0] and is_position_passed

    def check_wrong_chord_token_generated(self, token):
        """
        all chord tokens should be teacher forced
        """
        return TOKEN_OFFSET.CHORD_START.value <= token <= TOKEN_OFFSET.CHORD_END.value

    def check_wrong_eos_generated(self, token):
        return self.check_remnant_chord() and token == TOKEN_OFFSET.EOS.value

    def check_wrong_bar_token_generated(self, token):
        return not self.check_remnant_chord() and token == TOKEN_OFFSET.BAR.value
    
    def check_bar_generated(self, token):
        return token == TOKEN_OFFSET.BAR.value

    def teach_bar(self):
        token = TOKEN_OFFSET.BAR.value
        self.next_tokens_forced.append([token, 0, 0, 0])
        self.teach_chord_position()

    # def teach_first_position(self) -> None:
    #     """
    #     teach 1/128 position right after a bar token
    #     """
    #     self.next_tokens_forced.append(int(TOKEN_OFFSET.POSITION.value))

    # def teach_chord_token(self):
    #     next_chord_tokens = self.chord_token.pop(0)
    #     self.next_tokens_forced.append(next_chord_tokens)
    #     self.chord_position.pop(0)
    #     self.inter_chord_flags.pop(0)

    def teach_chord_position(self):
        next_chord_tokens = self.chord_token.pop(0)
        next_position_token = self.chord_position.pop(0)
        self.inter_chord_flags.pop(0)
        self.next_tokens_forced.append([next_position_token, next_chord_tokens, 0, 0])

    def teach_wrong_chord_token(self, wrong_token):
        self.no_sequence_appended = True

    def teach_remnant_chord(self):
        if len(self.inter_chord_flags) == 0:
            self.teach_eos()
            return
        if self.inter_chord_flags[0]:
            self.teach_chord_position()
        else:
            self.teach_bar()

    def teach_eos(self):
        token = TOKEN_OFFSET.EOS.value
        self.next_tokens_forced.append([token, 0, 0, 0])

    def validate_teacher_forced_sequence(self, seq) -> None:
        def _count_num_chord(seq):
            chord_counter = 0
            for token in seq:
                if TOKEN_OFFSET.CHORD_START.value <= token <= TOKEN_OFFSET.CHORD_END.value:
                    chord_counter += 1
            return chord_counter

        num_bars = seq.count(TOKEN_OFFSET.BAR.value)
        num_chord = _count_num_chord(seq)

        if len(self.chord_token) != 0:
            raise Exception(
                f"remnant chord length: {len(self.chord_token)} \n" "error in teacher forcing"
            )
        elif num_bars != int(math.ceil(self.input_data.num_measures)):
            raise Exception(f"bar length: {num_bars} \n" "error in bar length")
        elif num_chord != self.chord_length:
            raise Exception(
                f"num_chord: {num_chord} vs {self.chord_length} \n" "error in chord length"
            )
        else:
            logger.info(f"correct_length: {num_bars}")
            logger.info(seq)


class InferenceTask:
    def __init__(self, device: torch.device):
        self.device = device

    def __call__(
        self,
        model: MemTransformerLM,
        input_data: TransXlInputData,
        inference_cfg: yacs.config.CfgNode,
    ):
        self.model = model
        self.input_data = input_data
        self.inference_cfg = inference_cfg

    def init_seq_and_mems(
        self, encoded_meta_in: List[int], num_conditional_tokens: int
    ) -> Tuple[List[int], torch.Tensor]:
        encoded_meta = [[token, 0, 0, 0] for token in encoded_meta_in]
        seq = [[0, 0, 0, 0]]
        ctx = np.array(seq + encoded_meta[: num_conditional_tokens - 1], dtype=np.int32)[
            :, np.newaxis, :
        ]
        context = torch.from_numpy(ctx).to(self.device).type(torch.long)
        _, init_mems = self.model.forward_generate(context, mems=None)
        init_seq = seq + encoded_meta[:num_conditional_tokens]
        return init_seq, init_mems

    def calc_logits_and_mems(
        self, seq: List[int], mems: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        inp = np.array([seq[-1]], dtype=np.int32)[:, np.newaxis, :]
        input_token = torch.from_numpy(inp).to(self.device).type(torch.long)
        ret = self.model.forward_generate(input_token, mems)
        all_logits, mems = ret
        logits = [logit[-1, 0][1:] for logit in all_logits]
        return logits, mems

    def calc_probs(self, logits):
        # Handle temp 0 (argmax) case
        probs = []
        for i in range(4):
            if self.input_data.temperature == 0:
                prob = torch.zeros_like(logits[i])
                prob[logits[i].argmax()] = 1.0
            else:
                # Apply temperature spec
                logits[i] /= self.input_data.temperature
                # Compute softmax
                prob = F.softmax(logits[i], dim=-1)
            probs.append(F.pad(prob, [1, 0]))

        return probs

    def apply_sampling(self, probs):
        for prob in probs:
            _, top_idx = torch.topk(prob, self.input_data.top_k)
            mask = torch.zeros_like(prob)
            mask[top_idx] = 1.0
            prob *= mask
            prob /= torch.sum(prob)
        return probs

    def infer_token(self, probs):
        tokens = []
        for prob in probs:
            token = torch.multinomial(prob, 1)
            tokens.append(int(token.item()))
        return tokens

    def shift_token(self, tokens):
        assert tokens[0] <= 299
        if tokens[0] >= 3 and tokens[0] <= 171:
            tokens[0] += 557
        elif tokens[0] >= 172 and tokens[0] <= 299:
            tokens[0] += 260
        
        assert tokens[1] <= 173
        if tokens[1] >= 1 and tokens[1] <= 109:
            tokens[1] += 194
        elif tokens[1] >= 110 and tokens[1] <= 173:
            tokens[1] += 21
        
        assert tokens[2] <= 128
        if tokens[2] >= 1 and tokens[2] <= 128:
            tokens[2] += 2
        
        assert tokens[3] <= 128
        if tokens[3] >= 1 and tokens[3] <= 128:
            tokens[3] += 303
        
        return tokens

    def generate_sequence(self, seq, mems):
        logits = None
        teacher = TeacherForceTask(self.input_data)
        first_loop = True
        for _ in range(self.inference_cfg.GENERATION.generation_length):
            if seq[-1][0] == 1:
                break
            if teacher.next_tokens_forced:
                next_token = teacher.next_tokens_forced.pop(0)
                seq.append(next_token)
                logits, mems = self.calc_logits_and_mems(seq, mems)
                continue

            if teacher.no_sequence_appended:
                assert logits is not None
                teacher.no_sequence_appended = False
            elif first_loop:
                logits, _ = self.calc_logits_and_mems(seq, mems)
                first_loop = False
            else:
                logits, mems = self.calc_logits_and_mems(seq, mems)

            probs = self.calc_probs(logits)
            probs = self.apply_sampling(probs)

            # teacher forcing
            # in case with incomplete measure, trigger a flag after second bar token
            if not teacher.incomplete_filled:
                teacher.incomplete_filled = True if seq.count(TOKEN_OFFSET.BAR.value) > 1 else False

            # forcefully assign position 1/128 right after bar token
            if teacher.check_first_position(seq):
                teacher.teach_chord_position()
                continue

            # # in case there is one chord per bar
            # if teacher.check_one_chord_per_bar_case(seq):
            #     teacher.teach_chord_token()
            #     continue

            # # in case the chord changes within a bar
            # if teacher.check_mul_chord_per_bar_case(seq):
            #     teacher.teach_chord_token()
            #     continue

            # teacher forcing followed by token inference so that we can check if the wrong token was generated
            try:
                token = self.infer_token(probs)
                token = self.shift_token(token)
            except RuntimeError as e:
                logger.error(f"Sampling Error: {e}")
                seq = None
                break

            # generated token skipped necessary position
            if teacher.check_chord_position_passed(token[0]):
                teacher.teach_remnant_chord()
                continue

            # bar token generated but num measures exceed
            if teacher.check_wrong_bar_token_generated(token[0]):
                teacher.teach_eos()
                continue

            if teacher.check_bar_generated(token[0]):
                teacher.teach_remnant_chord()
                continue

            # wrong chord token generated
            if teacher.check_wrong_chord_token_generated(token[1]):
                teacher.teach_remnant_chord()
                continue

            # eos generated but we got more chords to write
            if teacher.check_wrong_eos_generated(token[0]):
                teacher.teach_remnant_chord()
                continue

            seq.append(token)

        try:
            seq = [num for group in seq for num in group]
            seq = seq[:-3]
            seq = [0] + list(filter(lambda t: t != 0, seq))
            teacher.validate_teacher_forced_sequence(seq)
        except Exception as error_message:
            logger.error(error_message)
            seq = None
        return seq

    def validate_generated_sequence(self, seq: List[int]) -> bool:
        num_note = 0
        for idx, token in enumerate(seq):
            if idx + 2 > len(seq) - 1:
                break
            if token in range(TOKEN_OFFSET.NOTE_VELOCITY.value, TOKEN_OFFSET.CHORD_START.value):
                if (
                    seq[idx - 1] in range(TOKEN_OFFSET.POSITION.value, TOKEN_OFFSET.BPM.value)
                    and seq[idx + 1]
                    in range(TOKEN_OFFSET.PITCH.value, TOKEN_OFFSET.NOTE_VELOCITY.value)
                    and seq[idx + 2]
                    in range(TOKEN_OFFSET.NOTE_DURATION.value, TOKEN_OFFSET.POSITION.value)
                ):
                    num_note += 1
        return num_note > 0

    def execute(self, encoded_meta) -> List[List[int]]:
        num_conditional_tokens = len(encoded_meta)
        idx = 0
        sequences = []
        while idx != self.input_data.num_generate:
            with torch.no_grad():
                logger.info("Generating the idx: " + str(idx + 1))
                seq, mems = self.init_seq_and_mems(encoded_meta, num_conditional_tokens)
                seq = self.generate_sequence(seq, mems)
                if seq is None:
                    continue
                if not self.validate_generated_sequence(seq):
                    logger.error("Empty sequence generated")
                    continue
            sequences.append(seq)
            idx += 1
        return sequences
