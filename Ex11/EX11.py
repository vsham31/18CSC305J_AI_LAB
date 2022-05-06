import tensorflow as tf

from utils.DL_utils import myCallback, build_model, compile_train_model, plot_loss_acc

from itertools import product

accuracy_desired = [0.85,0.9,0.95]

num_neurons = [16,32,64,128]

cases = list(product(accuracy_desired,num_neurons))

print("So, the cases we are considering are as follows...\n")

for i,c in enumerate(cases):

print("Accuracy target {}, number of neurons: {}".format(c[0],c[1]))

if (i+1)%4==0 and (i+1)!=len(cases):

print("-"*50)

for c in cases:

# Create a mycallback class with the specific accuracy target

callbacks = myCallback(c[0], print_msg=False)

# Build a model with a specific number of neurons

model = build_model(num_layers=1,architecture=[c[1]])

# Compile and train the model passing on the callback class,choose suitable batch size and a max

epoch limit

model = compile_train_model(model, x_train,y_train,callbacks=callbacks,

batch_size=32,epochs=30)

# Construct a suitable title string for displaying the results properly

title = "Loss and accuracy over the epochs for\naccuracy threshold \

{} and number of neurons {}".format(c[0],c[1])

# Use the plotting utility function, pass on the accuracy target,

# trained model, and the custom title string

plot_loss_acc(model,target_acc=c[0],title=title)
