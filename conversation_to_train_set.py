
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as Soup






class QA(object):
    
    def __init__(self, cps):
        self.cps = cps
        self.current = cps[0][0]
        self.current_q = ''
        self.current_a = ''
        self.answered = 0
        
    
    @classmethod
    def from_cps_data_frame(cls, cps_df):
        '''
            conversation_parts_dataframe :
            
            author_type   body                 created_at
            people        question_body        2017-04-15T01:09:45.000+08:00 
            people        question_body        2017-04-15T01:09:45.000+08:00 
            admin         answer_body          2017-04-15T01:09:45.000+08:00
            
            
        
        '''
        sorted_cps = cps_df.sort("created_at")
        cps_tuple_list = zip(sorted_cps["author_type"], [Soup("<html>%s</html>"%body).text.replace("nan","") for body in sorted_cps["body"]])

        return cls(cps_tuple_list)
    
    
        
    
    def __iter__(self):

        for cp in self.cps:

            if cp[0] == self.current:
                if cp[0] =='people':
                    self.current_q = "%s %s"%(self.current_q, cp[1])
                else:
                    self.current_a = "%s %s"%(self.current_a, cp[1])
            
            else:

                if cp[0] =='admin':
                    self.current_a = "%s %s"%(self.current_a, cp[1])
                    self.current = 'admin'
                    
                else:
                    
                    yield self.current_q ,self.current_a
                    
                    self.current = cp[0]
                    self.current_q = cp[1]
                    self.current_a = ''
                    
            

Total_QAS = []

conversation_data = pd.read_csv("query_result_2017-05-24T10-07-05.780Z.csv")

for conversation_uuid in conversation_data['conversation_uuid'].unique():
    cps = conversation_data[conversation_data['conversation_uuid']==conversation_uuid]
    qa = QA.from_cps_data_frame(cps)
    
    for q,a in qa:
        Total_QAS.append({"Question":q,"Answer":a})
    

    
    

        






