# Neural Networks

Neural networks are computational models inspired by the structure of biological neural networks in the brain. They form the foundation of deep learning and have achieved state-of-the-art results in image recognition, natural language processing, speech recognition, and generative AI.

## Basic Architecture

A neural network consists of layers of interconnected nodes (neurons). Each connection has a weight, and each neuron has a bias. The basic architecture includes an input layer, one or more hidden layers, and an output layer. A network with more than one hidden layer is called a deep neural network.

Each neuron computes a weighted sum of its inputs, adds a bias, and applies an activation function. The activation function introduces non-linearity, allowing the network to learn complex patterns. Common activation functions include ReLU (Rectified Linear Unit, f(x) = max(0, x)), sigmoid (f(x) = 1/(1+e^-x)), and tanh.

## Backpropagation

Backpropagation is the algorithm used to train neural networks. It works by computing the gradient of the loss function with respect to each weight using the chain rule of calculus, then updating weights in the direction that reduces the loss. The process has two phases: forward pass (computing predictions) and backward pass (computing gradients).

The learning rate controls how large the weight updates are. A learning rate too high causes divergence; too low causes slow convergence. Optimizers like Adam, RMSprop, and SGD with momentum adaptively adjust learning rates during training.

## Vanishing and Exploding Gradients

The vanishing gradient problem occurs when gradients become extremely small as they propagate backward through many layers, effectively stopping learning in early layers. This is especially problematic with sigmoid and tanh activations. ReLU activation largely solved the vanishing gradient problem for feedforward networks.

The exploding gradient problem is the opposite — gradients grow exponentially large, causing numerical instability and wild weight updates. Gradient clipping (capping gradients at a maximum value) is a common solution. Batch normalization also helps by normalizing activations at each layer.

## Convolutional Neural Networks (CNNs)

CNNs are designed for processing grid-like data such as images. They use convolutional layers that apply learnable filters (kernels) across the input, detecting features like edges, textures, and patterns. Key components include:

- **Convolutional layers**: Apply filters to detect local features. A 3x3 filter slides across the image computing dot products.
- **Pooling layers**: Reduce spatial dimensions. Max pooling takes the maximum value in each region; average pooling takes the mean.
- **Fully connected layers**: After feature extraction, these layers perform classification.

Popular CNN architectures include LeNet, AlexNet, VGGNet, ResNet, and Inception. ResNet introduced skip connections (residual connections) that allow training of very deep networks (100+ layers) by providing shortcut paths for gradients.

## Recurrent Neural Networks (RNNs)

RNNs are designed for sequential data like text, time series, and speech. They maintain a hidden state that acts as memory, processing one element at a time and updating the state. This allows them to capture temporal dependencies.

Vanilla RNNs struggle with long-range dependencies due to vanishing gradients. Long Short-Term Memory (LSTM) networks solve this with a gating mechanism consisting of forget, input, and output gates that control information flow. Gated Recurrent Units (GRU) are a simplified variant with fewer parameters.

## Transformers

Transformers replaced RNNs for most sequence tasks. They use self-attention mechanisms to process all positions in a sequence simultaneously, enabling parallelization. The key innovation is the attention mechanism: Query, Key, Value matrices are used to compute attention weights, allowing the model to focus on relevant parts of the input.

BERT (Bidirectional Encoder Representations from Transformers) and GPT (Generative Pre-trained Transformer) are transformer-based models that revolutionized NLP. Transformers are also used in vision (Vision Transformer / ViT) and multimodal tasks.

## Dropout and Regularization in Neural Networks

Dropout is a regularization technique that randomly deactivates a fraction of neurons during training, preventing co-adaptation and reducing overfitting. Typical dropout rates are 0.2-0.5. Other regularization techniques include weight decay (L2 regularization on weights), early stopping (stopping training when validation loss stops improving), and data augmentation.
