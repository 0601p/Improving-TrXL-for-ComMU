from model.multi_scale_ori import *
from model.ori import *
import torch
import numpy as np
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, random_split
import tqdm
import torch.nn.functional as F
from dataset import Commu_real, Commu_fake
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--midi_dir', type=str,
                help='midi_dir')
parser.add_argument('--meta_dir', type=str,
                help='meta_dir')
parser.add_argument('--meta_num', type=int, default=1,
                help='what kind of meta data you want to evaluate?')

parser = parser.parse_args()
meta_list_string = ["BPM","KEY",'TIMESIGNATURE','PITCHRANGE','NUMBEROFMEASURE',
             'INSTRUMENT','GENRE','MINVELOCITY','MAXVELOCITY','TRACKROLE',
             'RHYTHM']
meta_label_num = {"BPM":10,
                  "KEY":5,
                  'TIMESIGNATURE':4,
                  'PITCHRANGE':8,
                  'NUMBEROFMEASURE':3,
                 'INSTRUMENT':9,
                'GENRE':3,
                'MINVELOCITY':13,
                'MAXVELOCITY':13,
                'TRACKROLE':7,
                'RHYTHM':3}


print("loading dataset...")
real_meta_npy_ = np.load("./output_npy_/input_train.npy", allow_pickle=True)
real_midi_npy_ = np.load("./output_npy_/target_train.npy", allow_pickle=True)

fake_midi_dir = parser.midi_dir
fake_meta_dir = parser.meta_dir

fake_meta_npy_ = np.load(fake_meta_dir, allow_pickle=True)
fake_midi_npy_ = np.load(fake_midi_dir, allow_pickle=True)

dataset_size = len(real_midi_npy_)
train_size = int(dataset_size * 0.8)
validation_size = int(dataset_size * 0.2)
train_dataset, validation_dataset, test_dataset = random_split(dataset, [train_size, validation_size, test_size])



val_meta_npy_ = np.load("./output_npy_/input_val.npy", allow_pickle=True)
val_midi_npy_ = np.load("./output_npy_/target_val.npy", allow_pickle=True)
print("")

bs = 726

real_data = Commu_real(real_meta_npy_, real_midi_npy_,512) #to train real_model
dataset_size = len(real_data)
train_size = int(dataset_size * 0.8)
validation_size = int(dataset_size * 0.2)
real_train_dataset, real_validation_dataset = random_split(real_data, [train_size, validation_size])

real_train_loader = DataLoader(real_train_dataset, batch_size=bs, shuffle=True)
real_val_loader = DataLoader(real_validation_dataset, batch_size=bs, shuffle=True)

# fake_data = Commu(fake_meta_npy_, fake_midi_npy_,512) #to train real_model
# fake_loader = DataLoader(fake_data, batch_size=256, shuffle=True)

fake_data = Commu_fake(fake_meta_npy_, fake_midi_npy_,512) #to train real_model

fake_train_dataset, fake_validation_dataset = random_split(fake_data, [train_size, validation_size])
fake_train_loader = DataLoader(fake_data, batch_size=bs, shuffle=True)
fake_val_loader = DataLoader(fake_validation_dataset, batch_size=bs, shuffle=True)


test_data = Commu_real(val_meta_npy_, val_midi_npy_,512) #to compute CAS
test_loader = DataLoader(test_data, batch_size=bs, shuffle=True)

meta_num = parser.meta_num

print("loading model...")
# msresnet_real = MSResNet(input_channel=1, layers=[1, 1, 1, 1], num_classes=meta_label_num[meta_list_string[meta_num]])
# msresnet_real = msresnet_real.cuda()
msresnet_real = Regressor(meta_label_num[meta_list_string[meta_num]])
msresnet_real = msresnet_real.cuda()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(msresnet_real.parameters(), lr=0.001, momentum=0.9)
num_epochs = 50

print(f"training for {meta_list_string[meta_num]} which have {meta_label_num[meta_list_string[meta_num]]} labels")
print("training model with real dataset...")

best_validation_accuracy_real = 0
for epoch in range(num_epochs):  
    running_loss = 0.0
    for i, data in enumerate(tqdm.tqdm(real_loader)):
        msresnet_real.train()
        # get the inputs; data is a list of [inputs, labels]
        midi,label = data
        midi = midi.cuda()
        label = label.cuda()[:,meta_num]
        
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        # outputs = msresnet_real(midi)[0]
        outputs = msresnet_real(midi)
        loss = criterion(outputs, label.long())
        loss.backward()
        optimizer.step()
        # print statistics
        running_loss += loss.item()
        # if i % 2000 == 1999:    # print every 2000 mini-batches
        #     print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
        #     running_loss = 0.0
    if epoch % 6 == 5:
        print(running_loss)

    val_num = 0
    correct_num = 0
    with torch.no_grad():
        msresnet_real.eval()
        for i, data in enumerate(val_loader):
            midi,label = data
            midi = midi.cuda()
            label = label[:,meta_num]
            num = label.shape[0]
            val_num += num
            # outputs = msresnet_real(midi)[0].argmax(1).cpu()
            outputs = msresnet_real(midi).argmax(1).cpu()
            correct_num += sum(outputs==label)
        cur_accuracy = correct_num/val_num
        if cur_accuracy> best_validation_accuracy_real:
            best_validation_accuracy_real = cur_accuracy
        print(f"validation accuracy for epoch {epoch} is : {cur_accuracy}")
print('Finished Training real model')
msresnet_real = msresnet_real.to('cpu')

# msresnet_fake = MSResNet(input_channel=1, layers=[1, 1, 1, 1], num_classes=meta_label_num[meta_list_string[meta_num]])
# msresnet_fake = msresnet_fake.cuda()
msresnet_fake = Regressor(meta_label_num[meta_list_string[meta_num]])
msresnet_fake = msresnet_fake.cuda()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(msresnet_fake.parameters(), lr=0.001, momentum=0.9)

print(f"training for {meta_list_string[meta_num]} which have {meta_label_num[meta_list_string[meta_num]]} labels")
print("training model with fake dataset...")
best_validation_accuracy_fake = 0
for epoch in range(num_epochs):  
    running_loss = 0.0
    for i, data in enumerate(tqdm.tqdm(fake_loader)):
        msresnet_fake.train()
        # get the inputs; data is a list of [inputs, labels]
        midi,label = data
        midi = midi.cuda()
        label = label.cuda()[:,meta_num]
        
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        # outputs = msresnet_fake(midi)[0]
        outputs = msresnet_fake(midi)
        loss = criterion(outputs, label.long())
        loss.backward()
        optimizer.step()
        # print statistics
        running_loss += loss.item()
        # if i % 2000 == 1999:    # print every 2000 mini-batches
        #     print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
        #     running_loss = 0.0
    if epoch % 6 == 5:
        print(running_loss)

    val_num = 0
    correct_num = 0
    with torch.no_grad():
        msresnet_fake.eval()
        for i, data in enumerate(val_loader):
            midi,label = data
            midi = midi.cuda()
            label = label[:,meta_num]
            num = label.shape[0]
            val_num += num
            # outputs = msresnet_fake(midi)[0].argmax(1).cpu()
            outputs = msresnet_fake(midi).argmax(1).cpu()
            correct_num += sum(outputs==label)
        cur_accuracy = correct_num/val_num
        if cur_accuracy> best_validation_accuracy_fake:
            best_validation_accuracy_fake = cur_accuracy
        print(f"validation accuracy for epoch {epoch} is : {cur_accuracy}")  
print('Finished Training fake model')

print(f"best_validation_accuracy_real for real data is {best_validation_accuracy_real}")
print(f"best_validation_accuracy_fake for real data is {best_validation_accuracy_fake}")


# if __name__ == '__main__':

    # train_evaluate(parser)