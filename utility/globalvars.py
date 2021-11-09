globalVar = 0

max_len = 1024
nb_features = 36

nb_attention_param = 256
attention_init_value = 1.0 / 256
nb_hidden_units = 512   # number of hidden layer units
dropout_rate = 0.5
nb_lstm_cells = 128
nb_classes = 7

frame_size = 0.025  # 25 msec segments
step = 0.01     # 10 msec time step

### environment
dataset = 'berlin'
feature_extract=True
load_data=True
train_data_path='data/wav/'
top_n=7
