# -*- coding: utf-8 -*-
#
# File : core/deeplearning/HPConvNet.py
# Description : DeepLearning Convolutional Neural Network model.
# Date : 12th may 2017.
#
# This file is part of HomePod.
#
# Copyright Nils Schaetti <n.schaetti@gmail.com>

import torch
import torch.nn as nn
import torch.nn.functional as F


class PAN17ConvNet(nn.Module):

    # Constructor
    def __init__(self, n_classes=2, params=(4800, 400)):
        """
        Constructor
        """
        super(PAN17ConvNet, self).__init__()

        # 2D convolution layer, 1 in channel, 10 out channels (filters), kernel size 5
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5, stride=1)

        # 2D convolution layer, 10 input channels, 20 output channels (filters), kernel size 5
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)

        # 2D Dropout layer, with probability of an element to be zeroed to 0.5
        self.conv2_drop = nn.Dropout2d()

        # Linear transformation with 4800 inputs features and 50 output features
        self.fc1 = nn.Linear(params[0], params[1])

        # Linear transformation with 50 inputs features and 2 output features
        self.fc2 = nn.Linear(params[1], n_classes)
    # end __init__

    # Forward
    def forward(self, x):
        """
        Forward
        :param x:
        :return:
        """
        # ReLU << Max pooling 2D with kernel size 2 << Convolution layer 1 << x
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)

        # ReLU << Max pooling 2D with kernel size 2 << Dropout 2D << Convolution layer 2 << x
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))

        # Put all 320 features into 1D line << x
        x = x.view(-1, PAN17ConvNet.num_flat_features(x))

        # ReLU << Linear model on 4800 features to 50 outputs << x
        x = F.relu(self.fc1(x))

        # Trained dropout << x
        x = F.dropout(x, training=self.training)

        # Linear model on 50 features to 2 outputs
        x = self.fc2(x)

        # Softmax layer << x
        return F.log_softmax(x)
    # end forward

    # Number of flat features
    @staticmethod
    def num_flat_features(x):
        """
        Number of flat features.
        :param x:
        :return:
        """
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
    # end num_flat_features

# end PAN17ConvNet