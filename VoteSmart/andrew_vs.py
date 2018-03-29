from votesmart import votesmart
import numpy as np
import pandas as pd
import votesmart_api

votesmart.apikey = mykey

cands = votesmart.candidates()
# #for cand in cands.getByOfficeState(1):

rating = votesmart.rating.getCategories()

state = votesmart.state

# s = state.getStateIDs()
#
# snp = np.array(s)

stateIDS = []

states = votesmart.state.getStateIDs()

for s in states:
    stateIDS.append(s.stateId)

OfficeTypes = []
for t in votesmart.office.getTypes():
    OfficeTypes.append(t.officeTypeId)

count = 0
allcands = []


# for s in stateIDS:
#     for o in OfficeTypes:
#         try:
#             c = cands.getByOfficeTypeState(o, s, 2016)
#         except:
#             pass
#         for x in c:
#             name = u' '.join((x.firstName, x.lastName)).encode('utf-8').strip()
#             allcands.append(name)
#             print (count)
#             count +=1
#             if c>100:
#                 break

c = cands.getByOfficeTypeState(OfficeTypes[0], stateIDS[10], 2016)
for x in c:
    name = u' '.join((x.firstName, x.lastName)).encode('utf-8').strip()
    allcands.append(name)

listallcands = list(set(allcands))
df = pd.DataFrame(listallcands)

for cand in allcands:
    print (cand.getCandidateRating())
