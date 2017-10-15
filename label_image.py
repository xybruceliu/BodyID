import tensorflow as tf, sys
import os

"""
docker run -it -v $HOME/tf_files:/tf_files gcr.io/tensorflow/tensorflow:latest-devel

cd /tensorflow
git pull


python tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=/tf_files/bottlenecks --how_many_training_steps=4000 --learning_rate=0.005 --model_dir=/tf_files/inception --output_graph=/tf_files/retrained_graph.pb --output_labels=/tf_files/retrained_labels.txt --image_dir=/tf_files/images


python /tf_files/label_image.py/tf_files/flower_photos/daisy/test.jpg

"""

#image_path = "/Users/xingyuliu/tf_files/flower_photos/daisy/test.jpg"

def label(image_path):

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("/Users/xingyuliu/tf_files/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("/Users/xingyuliu/tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        human_string = (label_lines[top_k[0]], label_lines[top_k[1]]) 
        score = (predictions[0][top_k[0]], predictions[0][top_k[1]])
        
        return (human_string[0], score[0], human_string[1], score[1])
    
