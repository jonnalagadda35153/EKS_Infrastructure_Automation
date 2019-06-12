import boto3
import json
import re
import time
import sys
import yaml
#from ruamel.yaml import YAML

autoscale_client = boto3.client('autoscaling')
eks_client = boto3.client('eks')

#Retriving a dictionry of autosclaing groups
autoscaling_response = autoscale_client.describe_auto_scaling_groups()
#Retriving a dictionry of EKS clusters
eks_response = eks_client.list_clusters()

#-----Autoscaling Groups------#
#Retriving AutoscalingGroups Data ignoring meta data
autoscaling = autoscaling_response['AutoScalingGroups']
autoscaling_groups = []
#Creating a list of autoscaling group names
for i in range(0,len(autoscaling)):
    autoscaling_groups.append(autoscaling_response['AutoScalingGroups'][i]['AutoScalingGroupName'])
    #print(autoscaling_response['AutoScalingGroups'][i]['AutoScalingGroupName'])

#-----EKS clusters------#
#Appending Autoscaling group for Clusterautoscaling.yml
eks_clusters = []
for i in range(0,len(eks_response['clusters'])):
    eks_clusters.append(eks_response['clusters'][i])
    print()
    print(eks_response['clusters'][i])
    r = re.compile('eksctl-'+eks_response['clusters'][i])
    asg_list = list(filter(r.match, autoscaling_groups))
    print(asg_list)
    stream = open('cluster_autoscaler.yml','r')
    i = 0
    for d in yaml.load_all(stream):
        i = i + 1
        if i == 6:
            for item in d['spec']['template']['spec']['containers']:
                for a in range(0,2):
                    item['command'][5] = "--nodes=2:10:" + asg_list[a]
                    write_2 = open('cluster_autoscale_2.yml','w')
                    yaml.dump_all([d], write_2, default_flow_style=False, explicit_start=True)
                    fin = open("cluster_autoscale_1.yml", "r")
                    d1 = fin.read()
                    fin.close()
                    fin = open("cluster_autoscale_2.yml", "r")
                    d2 = fin.read()
                    fin.close()
                    combine_data = d1 + d2
                    fout = open('cluster_auto.yml','w')
                    fout.write(combine_data)
                    fout.close()
                    time.sleep(10)
                    '''
                    with open('final_cluster_auto.yml', 'w') as outfile:
                        print("Into combinig files")
                        for fname in filenames:
                            print(fname)
                            with open(fname) as infile:
                                outfile.write(infile.read())
                    '''
                        
