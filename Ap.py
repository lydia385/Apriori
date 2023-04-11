import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import itertools
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


def support(transactions , min_support):
  itemset=set([item for sublist in transactions for item in sublist])
  count_items={}
  for item in itemset :
    count=0
    for transaction in transactions :
      set_t=set(transaction)
      if item in transaction :
        count+=1
        
    support = count/len(transactions)
    #filter items that have support > min_support
    
    if min_support <= support and support!=1:
      count_items[item]=support
  count_items=pd.DataFrame.from_dict(count_items,orient='index')
  return count_items


def create_itemsets(items,k):
  # items=support.index
  perm_set = itertools.combinations(items,k)
  return set(perm_set)



def support_itemsets(transactions , itemsets , min_support):
  count_items={}
  for item in itemsets :
    count=0
    i_set=set(item)
    for transaction in transactions :
      t_set=set(transaction)
      if t_set.intersection(i_set)==i_set :
        count+=1
    support = count/len(transactions)
    #filter items that have support > min_support
    if min_support <= support and support!=1:
       count_items[item]=support
    
  count_items=pd.DataFrame.from_dict(count_items,orient='index')
  return count_items


def apriori(df,min_support):
  transactions_new = df.copy()
  for c in transactions_new .columns:
      transactions_new[c]=str(c)+"="+transactions_new[c].apply(str)
  transactions=transactions_new.to_numpy()
  item_sep=support(transactions,min_support)
  if  min_support>0 :
        k=2
        itemset=item_sep.index
        df=pd.DataFrame()
        while len(item_sep)!=0:
          itemsets=create_itemsets(itemset,k)
          item_sep=support_itemsets(transactions,itemsets,min_support)

          if not item_sep.empty:
              itemset=list()
              for i in item_sep.index:
                for g in i:
                    itemset.append(g)
              itemset=set(itemset)
          k+=1
        
        it=len(itemset)+1
        if len(itemset):
          for i in range(1,it):
            itemsets=create_itemsets(itemset,i)
            item_sep=support_itemsets(transactions,itemsets,min_support)
            df=pd.concat([item_sep,df])
          df=df.reset_index()
          df.columns=["itemsets","support"]
        else :
          print("error")
  else : return "error"

  return df,itemset



def support_items(transactions , min_support):
      count_items={}
      itemsets=set([item for sublist in transactions for item in sublist])
      for item in itemsets:
        itemset = frozenset([item])
        support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / len(transactions)
        
        if support >= min_support:
            count_items[itemset] = support
      return  count_items


def support_iteamset(transactions,itemsets,min_support):
        frequent_itemsets_k = {}
        taille = len(transactions)
        for itemset in itemsets:
            support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / taille
            if support >= min_support:
                frequent_itemsets_k[itemset] = support
        return frequent_itemsets_k

def Remove(frequent_itemsets):
   reduced ={}
   for itemset1 in frequent_itemsets:
            redundant = False
            for itemset2 in frequent_itemsets:
                if itemset1 != itemset2 and itemset1.issubset(itemset2) and frequent_itemsets[itemset1] == frequent_itemsets[itemset2]:
                    redundant = True
                    break
            if not redundant:
                reduced[itemset1] = frequent_itemsets[itemset1]
   return reduced


def close(transactions, min_support):

    
    closed_frequent_itemsets = support_items(transactions , min_support)
  
    k = 2
    while True:
        itemsets = create_itemsets(closed_frequent_itemsets,k)
        if len(itemsets) == 0:
            break
        
        frequent_itemsets = support_iteamset(transactions ,itemsets, min_support)
        if len(frequent_itemsets) == 0:
            break
        
        frequent_itemsets_reduced = Remove(frequent_itemsets)


        closed_frequent_itemsets.update(frequent_itemsets_reduced)
        
        k += 1
    
    return closed_frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence,metric='confidence'):
    # sort frequent itemsets by descending support
    if(frequent_itemsets.shape[0] > 0):
        frequent_itemsets.columns=["itemsets","support"]
        frequent_itemsets = frequent_itemsets.sort_values('support', ascending=False)
        rules = []
        for i in range(len(frequent_itemsets)):
            # generate all non-empty subsets of itemset
            itemset = tuple(frequent_itemsets.iloc[i]['itemsets'])
            for j in range(1, len(itemset)):
                for subset in itertools.combinations(itemset, j):
                    subset = tuple(subset)
                    # calculate confidence of rule
                    support_itemset = frequent_itemsets[frequent_itemsets['itemsets'] == itemset]['support'].values
                    support_subset = frequent_itemsets[frequent_itemsets['itemsets'] == subset]['support'].values
                    
                    if len(support_subset) == 0:
                        continue
                    confidence = support_itemset / support_subset[0]
                    if confidence >= min_confidence:
                        # add rule to list
                        support_consequent = frequent_itemsets[frequent_itemsets['itemsets'] == tuple(set(itemset) - set(subset))]['support'].values
                        lift = confidence / support_consequent
                        rules.append({
                            'antecedent': subset,
                            'consequent': set(itemset) - set(subset),
                            'support': support_itemset,
                            'confidence': confidence,
                            'lift' : lift
                        })
        # sort rules by descending confidence
        rules = pd.DataFrame(sorted(rules, key=lambda x: x['confidence'], reverse=True))
        return rules
    else:
         print("there is no association rules")
import pandas as pd
def autominsup(df):
  encoder=LabelEncoder()
  transactions =pd.DataFrame()
  for c in df.columns:
      transactions[c]=encoder.fit_transform(df[c])
  # Define a list of candidate minimum supports
  min_sup_list = [0.1, 0.05, 0.01, 0.005, 0.001]

  # Evaluate performance for each candidate minimum support
  best_min_sup = None
  best_metric = 0
  for min_sup in min_sup_list:
      # Run Apriori algorithm
      df,frequent_itemsets = apriori(transactions,min_sup)
          # Evaluate performance based on some metric (e.g. number of frequent itemsets)
      num_frequent_itemsets = len(frequent_itemsets)
      
      # Update best minimum support and metric if necessary
      if num_frequent_itemsets > best_metric:
          best_metric = num_frequent_itemsets
          best_min_sup = min_sup
  return best_min_sup

  # Use the best minimum support for the final Apriori run
