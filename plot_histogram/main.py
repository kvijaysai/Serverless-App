
from flask import escape
import matplotlib.pyplot as plt
import io
from google.cloud import storage


def plot_hist(request):
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'data' in request_json:
        data = eval(request_json['data'])
        link = request_json['link']
    elif request_args and 'data' in request_args:
        data = eval(request_args['data'])
        link = request_args['link']
    else:
        data = 'L'
        link = 'N'
    
    plt.figure(figsize=(10,8))
    plt.bar(list(data.keys()), data.values(), color='g')
    plt.title("Distribution of Sentence Lengths", fontsize=20)
    plt.xlabel('Sentence Lengths', fontsize=18)
    plt.ylabel('Number of Occurences', fontsize=16)
    
    client = storage.Client(project='vijaysai')
    bucket_name = 'histimages_bucket'
    bucket = client.bucket(bucket_name)
    blob = bucket.blob('histogram_'+str(link)+'.png')
    
    # temporarily save image to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    
    # upload buffer contents to gcs
    blob.upload_from_string(
        buf.getvalue(),
        content_type='image/png')
    
    buf.close()
    
    # gcs url to uploaded matplotlib image
    url = blob.public_url
    
    return url