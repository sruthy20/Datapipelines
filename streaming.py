import random
import json
import time
import boto3

class StreamInput():

  def __init__(self,cnt):
    self.cnt=cnt
  
  def data_gen(self):
    inp={}
    num1=random.randint(1,100)
    num2=random.randint(1,100)
    if self.cnt%2==0:
      val='Evn'
    else:
      val='odd'
    inp={'First_Num':num1,'Second_Num':num2,'Value':val}  
    outrecords=json.dumps(inp)
    return {'Data': bytes(outrecords, 'utf-8')}

  def output(self):
    return [self.data_gen() for _ in range(self.cnt)]

def main():
  i=50
  Kinesisstream=boto3.client('firehose')

  while i>0:

    stream=StreamInput(3)
    records=stream.output()
    result = Kinesisstream.put_record_batch(DeliveryStreamName="SampleNumbers",
                                                      Records=records)
    i-=1
    time.sleep(0.1)

if __name__=='__main__':
  main()
