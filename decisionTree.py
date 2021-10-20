# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 20:57:33 2021

@author: Ziyuan
"""

import numpy as np 
from math import log
# loaddata 
def loaddata(name):
    data=np.loadtxt(open(name),dtype=str,delimiter='\t',skiprows=0)
    return data

# calc entropy  H(Y)
def calc_entropy(data):
    class_column=data[:,-1]
    attribute=list(set(x for x in class_column))
    typeA=0
    typeB=0
    for row in data:
        if row[-1]==attribute[0]:
            typeA+=1
        else:
            typeB+=1
    probA=typeA/(typeA+typeB)
    probB=typeB/(typeA+typeB)
    if probA==0 or probB==0:
        return 0
    entropy=-(probA*(log(probA)/log(2))+probB*(log(probB)/log(2)))
    return entropy

#calc H(Y|A) using data and which column we are insterested in 
#find the half last part of mutual info, minimize this part
def mutual_comp(data,n):
    """
    attribut=list(set(x for x in data[:,n]))   
    re_x=[]
    re_y=[]
    for row in data: 
        x=row[n]
        if(x==attribut[0]):
            re_x.append(row)
        else:
            re_y.append(row)
    n=len(re_x)
    m=len(re_y)
    if n==0 or m==0:
        return 0
    
    x_entro=calc_entropy(np.array(re_x))
    y_entro=calc_entropy(np.array(re_y))
    
    
    return n*x_entro/(n+m)+m*y_entro/(n+m)
    """
    attribut=list(set(x for x in data[:,n]))   
    re_x=[]
    re_y=[]
    for row in data: 
        x=row[n]
        if(x==attribut[0]):
            re_x.append(row)
        else:
            re_y.append(row)
    n=len(re_x)
    m=len(re_y)
    if n==0 or m==0:
        return 0
    
    x_entro=calc_entropy(np.array(re_x))
    y_entro=calc_entropy(np.array(re_y))
    
    
    return n*x_entro/(n+m)+m*y_entro/(n+m)
    
   
#taking data and used, and entropy as info
#loop through all columns that has not been used and find the one with lowest H(Y|X)
#double check if the mutual is >0 or not
def find_splitting_attri(data,used,entro):
    min_mut=1
    column=data.shape[1]-1
    result=-1
    if len(used)-1>=column:
        return -1
    for i in range(column):
        if i in used:
            continue
       
        re=mutual_comp(data,i)
        if re<=min_mut:
            min_mut=re
            result=i          
    if entro-min_mut<=0:
        return -1
    
    return result
    
#using data, column we are splitting o, specific attrbute we want to seperate out    
def splitting_data(data,split_col):
    left=[]
    right=[]
    attri=find_content(data, split_col)
    for row in data:
        if row[split_col]==attri[0]:
            left.append(row)    
        else: 
            right.append(row)
    return np.array(left),np.array(right)

# using attribute and find specific vote       
            


def find_content(data,n):
    re=list(set(x for x in data[:,n]))
    re.sort(reverse=False)
    return re

def find_major_vote(data):       
    re_dict={}
    for row in data: 
        re=row[-1] 
        if re in re_dict:
            re_dict[re]+=1
        else:
            re_dict[re]=1
    dict_sorted = sorted(re_dict.items(), key=lambda re_dict:re_dict[0],reverse = False) 
    y_max=0
    y_re=""
    for item in dict_sorted:
        if item[1]>=y_max:            
            y_re=item[0]
            y_max=item[1]
    return y_re

def find_num_vote(data):
    re_dict={}
    for row in data:
        re=row[-1]      
        if re in re_dict:
            re_dict[re]+=1
        else:
            re_dict[re]=1
         
    re=[]
    dict_sorted = sorted(re_dict.items(), key=lambda re_dict:re_dict[0],reverse = False)   
    for item in dict_sorted:
        new_str=str(item[1])+" "+item[0]
        re.append(new_str)       
    return re_dict


class Node(object):
    def __init__(self,left=None,right=None,data=None,splitting_point=None,max_depth=-1,tags=None,attributes=None,label_list=None):
        self.right=right
        self.left=left
        self.data=data
        self.attributes=attributes
        self.splitting_point=splitting_point
        #self.max_depth=max_depth
        self.tags=tags
        #self.label_list=label_list
      # attribute  

    
def decision_tree(used,data,depth,max_depth,previous_seperation,label_list,tags,last_attri):
  
    
    if(depth==0):
        last_attri=find_content(data, -1)
        dic=find_num_vote(data)
        st1=""
        st2=""
        
        if last_attri[0] in dic:
            st1=str(dic[last_attri[0]])+" "+last_attri[0]
        else:
            st1="0"+" "+last_attri[0]
        
        if last_attri[1] in dic:
            st2=str(dic[last_attri[1]])+" "+last_attri[1]
        else:
            st2="0"+" "+last_attri[1]
            
        print("["+st1+"/"+st2+"]")

    else:
        label=label_list[previous_seperation]
        
        dic=find_num_vote(data)
        st1=""
        st2=""
        
        if last_attri[0] in dic:
            st1=str(dic[last_attri[0]])+" "+last_attri[0]
        else:
            st1="0"+" "+last_attri[0]
        
        if last_attri[1] in dic:
            st2=str(dic[last_attri[1]])+" "+last_attri[1]
        else:
            st2="0"+" "+last_attri[1]
            
        print("|"*depth+label+'='+tags+": "+"["+st1+"/"+st2+"]")

    node=Node()    
    node.data=data
    node.label_list=label_list
    
    
    
    #stopping and calc related info for next splitting point
    if max_depth==0 or depth>=max_depth or depth>=data.shape[1]-1 or data.shape[0]<2:
        vote=find_major_vote(data)
        node.vote=vote  
        return node    
    entropy=calc_entropy(data)    
    column=find_splitting_attri(data, used, entropy)
    if column==-1:
        vote=find_major_vote(data)
        node.vote=vote  
        return node
    
    attribute=find_content(data,column)
    if len(attribute)!=2:
        vote=find_major_vote(data)
        node.vote=vote  
        return node
        
    node.splitting_point=column
    node.attributes=attribute
    used.append(column)
    #node的attribute本次分类使用什么，同时pass 到下一个decision tree做tag
    
       
    #setting next two nodes and call them
    
    data_left,data_right=splitting_data(data,column)
    node.left=decision_tree(used,data_left,depth+1,max_depth,column,label_list,attribute[0],last_attri)
    node.right=decision_tree(used,data_right,depth+1,max_depth,column,label_list,attribute[1],last_attri)
    return node
"""
def decision_tree(used,data,depth,max_depth,previous_seperation,label_list,tags):
  
    
    if(depth==0):
        print(find_num_vote(data))
    else:
        label=label_list[previous_seperation]
        print("|"*depth+label+'='+tags+":"+str(find_num_vote(data)))
    
    node=Node()    
    node.data=data
    node.label_list=label_list
    
    
    
    #stopping and calc related info for next splitting point
    if max_depth==0 or depth>=max_depth or depth>=data.shape[1]-1 or data.shape[0]<2:
        vote=find_major_vote(data) 
        node.vote=vote  
        return node    
    entropy=calc_entropy(data)    
    column=find_splitting_attri(data, used, entropy)
    if column==-1:
        vote=find_major_vote(data)
        node.vote=vote  
        return node
    
    attribute=find_content(data,column)
    node.splitting_point=column
    node.attributes=attribute
    used.append(column)
    #node的attribute本次分类使用什么，同时pass 到下一个decision tree做tag
    
       
    #setting next two nodes and call them
    
    data_left,data_right=splitting_data(data,column)
    node.left=decision_tree(used,data_left,depth+1,max_depth,column,label_list,attribute[0])
    if len(attribute)==2:
        node.right=decision_tree(used,data_right,depth+1,max_depth,column,label_list,attribute[1])
    return node
"""
def predict(node,row):
 
    if(node.left==None and node.right==None):
        return node.vote
    
    spli_n=node.splitting_point
    attribute=node.attributes
    if row[spli_n]==attribute[0]:
        
            return predict(node.left,row)
        
    else:
        
            return predict(node.right,row)
        
def predict_all(node,data):
    re=[]
    for row in data:
        re.append(predict(node,row))
    return re 

def find_error(data,vote):
    error=0
    for i in range(data.shape[0]):
        if data[i,-1]!=vote[i]:
            error+=1
    return error/data.shape[0] 

def metric_out(train_error, test_error, path):
    f=open(path,"w")
    f.write("error(train): "+str(train_error))
    f.write("\nerror(test): "+str(test_error))

def labelout(vote,path):
    f=open(path,"w+")
    for i in vote:
        f.write(i+'\n')
    f.close()

if __name__ == "__main__":
    inte=[0,1,2,4]
    pre_train=loaddata(r'C:\Users\Ziyuan\OneDrive\桌面\machine_learn\hw2\handout\mushroom_train.tsv')
    pre_test=loaddata(r'C:\Users\Ziyuan\OneDrive\桌面\machine_learn\hw2\handout\education_test.tsv')
    label_list=pre_train[0,:]
    train=pre_train[1:,:]
    for i

    
    