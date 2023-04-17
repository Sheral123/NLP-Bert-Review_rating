{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:30.618699Z\",\"iopub.execute_input\":\"2023-04-13T08:34:30.619177Z\",\"iopub.status.idle\":\"2023-04-13T08:34:30.667282Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:30.619131Z\",\"shell.execute_reply\":\"2023-04-13T08:34:30.666265Z\"}}\n# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python\n# For example, here's several helpful packages to load\n\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\n\n# Input data files are available in the read-only \"../input/\" directory\n# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory\n\nimport os\nfor dirname, _, filenames in os.walk('/kaggle/input'):\n    for filename in filenames:\n        print(os.path.join(dirname, filename))\n\n# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using \"Save & Run All\" \n# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:43.795393Z\",\"iopub.execute_input\":\"2023-04-13T08:34:43.795801Z\",\"iopub.status.idle\":\"2023-04-13T08:34:49.710275Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:43.795764Z\",\"shell.execute_reply\":\"2023-04-13T08:34:49.709154Z\"}}\nimport pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom transformers import BertTokenizer, TFBertForSequenceClassification\nimport tensorflow as tf\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:52.294679Z\",\"iopub.execute_input\":\"2023-04-13T08:34:52.295674Z\",\"iopub.status.idle\":\"2023-04-13T08:34:52.329802Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:52.295622Z\",\"shell.execute_reply\":\"2023-04-13T08:34:52.328807Z\"}}\n# Load the dataset\ndata = pd.read_csv('/kaggle/input/kaggle-wars-eclipse/train (1).csv')\n\n# Split the dataset into training and testing sets\n\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:37.269358Z\",\"iopub.status.idle\":\"2023-04-13T08:34:37.270163Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:37.269883Z\",\"shell.execute_reply\":\"2023-04-13T08:34:37.269910Z\"}}\ndata_rating_5 = data[data['Rating'] == 5]\ndata_not_5 = data[data['Rating'] != 5]\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:37.271589Z\",\"iopub.status.idle\":\"2023-04-13T08:34:37.272341Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:37.272080Z\",\"shell.execute_reply\":\"2023-04-13T08:34:37.272106Z\"}}\nfraction_to_keep = 0.35  # Change this value to the desired fraction of rows to keep\n\ndata_rating_5 = data_rating_5.sample(frac=fraction_to_keep, random_state=42)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:37.273750Z\",\"iopub.status.idle\":\"2023-04-13T08:34:37.274535Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:37.274262Z\",\"shell.execute_reply\":\"2023-04-13T08:34:37.274289Z\"}}\ndata_balanced = pd.concat([data_rating_5, data_not_5])\ndata_balanced = data_balanced.sample(frac=1, random_state=42).reset_index(drop=True)\n\n# %% [code]\nimport nltk\nimport re\nfrom nltk.corpus import stopwords\nfrom nltk.tokenize import word_tokenize\n\nnltk.download('punkt')\nnltk.download('stopwords')\n\ndef preprocess_text(text):\n    text = text.lower()\n    text = re.sub(r'\\W+', ' ', text)\n    tokens = word_tokenize(text)\n    stop_words = set(stopwords.words('english'))\n    tokens = [token for token in tokens if token not in stop_words]\n    return ' '.join(tokens)\n\ndata['cleaned_reviews'] = data['Review'].apply(preprocess_text)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:35:05.230352Z\",\"iopub.execute_input\":\"2023-04-13T08:35:05.231069Z\",\"iopub.status.idle\":\"2023-04-13T08:35:05.248966Z\",\"shell.execute_reply.started\":\"2023-04-13T08:35:05.231029Z\",\"shell.execute_reply\":\"2023-04-13T08:35:05.247769Z\"}}\ndata\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:35:08.184643Z\",\"iopub.execute_input\":\"2023-04-13T08:35:08.185618Z\",\"iopub.status.idle\":\"2023-04-13T08:35:08.197536Z\",\"shell.execute_reply.started\":\"2023-04-13T08:35:08.185564Z\",\"shell.execute_reply\":\"2023-04-13T08:35:08.196488Z\"}}\ntrain_data, test_data = train_test_split(data, test_size=0.2, random_state=42)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:35:10.476627Z\",\"iopub.execute_input\":\"2023-04-13T08:35:10.477069Z\",\"iopub.status.idle\":\"2023-04-13T08:35:48.452855Z\",\"shell.execute_reply.started\":\"2023-04-13T08:35:10.477022Z\",\"shell.execute_reply\":\"2023-04-13T08:35:48.451811Z\"}}\n# Define the tokenizer\ntokenizer = BertTokenizer.from_pretrained('bert-base-uncased')\n\n# Tokenize the reviews\ntrain_encodings = tokenizer(train_data['Review'].tolist(), truncation=True, padding=True, max_length=128)\ntest_encodings = tokenizer(test_data['Review'].tolist(), truncation=True, padding=True, max_length=128)\n\n# Create tf.data.Dataset\ntrain_labels = train_data['Rating'].to_numpy() - 1  # 0-indexed labels\ntest_labels = test_data['Rating'].to_numpy() - 1\n\ntrain_dataset = tf.data.Dataset.from_tensor_slices((\n    dict(train_encodings),\n    train_labels\n)).shuffle(1000).batch(8)\n\ntest_dataset = tf.data.Dataset.from_tensor_slices((\n    dict(test_encodings),\n    test_labels\n)).batch(8)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:35:52.858134Z\",\"iopub.execute_input\":\"2023-04-13T08:35:52.858617Z\",\"iopub.status.idle\":\"2023-04-13T09:37:48.419789Z\",\"shell.execute_reply.started\":\"2023-04-13T08:35:52.858570Z\",\"shell.execute_reply\":\"2023-04-13T09:37:48.418717Z\"}}\n# Initialize the model\nmodel = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)\n\n# Define the optimizer, loss function, and metrics\noptimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)\nloss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)\nmetrics = [tf.keras.metrics.SparseCategoricalAccuracy()]\n\n# Compile the model\nmodel.compile(optimizer=optimizer, loss=loss, metrics=metrics)\n\n# Train the model\nhistory = model.fit(train_dataset, epochs=10, validation_data=test_dataset)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T09:37:48.750106Z\",\"iopub.execute_input\":\"2023-04-13T09:37:48.750633Z\",\"iopub.status.idle\":\"2023-04-13T09:37:48.768148Z\",\"shell.execute_reply.started\":\"2023-04-13T09:37:48.750598Z\",\"shell.execute_reply\":\"2023-04-13T09:37:48.767153Z\"}}\ndata1 = pd.read_csv('/kaggle/input/kaggle-wars-eclipse/test (2).csv')\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T08:34:37.289414Z\",\"iopub.status.idle\":\"2023-04-13T08:34:37.290252Z\",\"shell.execute_reply.started\":\"2023-04-13T08:34:37.289994Z\",\"shell.execute_reply\":\"2023-04-13T08:34:37.290021Z\"}}\nimport re\nfrom nltk.corpus import stopwords\nfrom nltk.tokenize import word_tokenize\n\nnltk.download('punkt')\nnltk.download('stopwords')\n\ndef preprocess_text(text):\n    text = text.lower()\n    text = re.sub(r'\\W+', ' ', text)\n    tokens = word_tokenize(text)\n    stop_words = set(stopwords.words('english'))\n    tokens = [token for token in tokens if token not in stop_words]\n    return ' '.join(tokens)\n\ndata1['cleaned_reviews'] = data1['Review'].apply(preprocess_text)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T09:37:59.863519Z\",\"iopub.execute_input\":\"2023-04-13T09:37:59.864186Z\",\"iopub.status.idle\":\"2023-04-13T09:37:59.876716Z\",\"shell.execute_reply.started\":\"2023-04-13T09:37:59.864149Z\",\"shell.execute_reply\":\"2023-04-13T09:37:59.875610Z\"}}\ndata1\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-04-13T09:38:06.939588Z\",\"iopub.execute_input\":\"2023-04-13T09:38:06.940524Z\",\"iopub.status.idle\":\"2023-04-13T09:38:47.363680Z\",\"shell.execute_reply.started\":\"2023-04-13T09:38:06.940469Z\",\"shell.execute_reply\":\"2023-04-13T09:38:47.362634Z\"}}\ndef predict_batch(model, tokenized_texts, batch_size=32):\n    num_samples = len(tokenized_texts['input_ids'])\n    logits_list = []\n\n    for i in range(0, num_samples, batch_size):\n        batch = {\n            key: value[i:i + batch_size]\n            for key, value in tokenized_texts.items()\n        }\n\n        batch_logits = model(batch).logits\n        logits_list.append(batch_logits)\n\n    logits = np.vstack(logits_list)\n    return logits\n\n# Predict on the test dataset\ntest_reviews = data1['Review'].tolist()\ntest_tokens = tokenizer(test_reviews, truncation=True, padding=True, max_length=128, return_tensors='tf')\nlogits = predict_batch(model, test_tokens, batch_size=32)\npredictions = np.argmax(logits, axis=-1) + 1  # Convert back to 1-indexed labels\n\n# Save the predictions as a CSV file\noutput = pd.DataFrame({ 'Predicted_Rating': predictions})\noutput.to_csv('predictions111.csv', index=False)\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n\n\n# %% [code]\n","metadata":{"_uuid":"1ae1be90-a6a7-4bfa-87f6-d811f283bf7e","_cell_guid":"60156135-18e9-4b4d-a8e6-f8da031143bc","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}