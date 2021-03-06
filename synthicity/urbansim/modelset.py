import os, sys
import simplejson
from synthicity.utils import misc
import pandas as pd

if pd.version.version == "0.12.0":
  raise Exception("ERROR: Seriously, don't blame me, but Pandas .12 is broken")

{% if saveoutput %}
num = misc.get_run_number()
{% endif %}

{% if pathinsertcwd %}
sys.path.insert(0,".")
{% endif %}
import dataset
dset = dataset.{{dataset}}(os.path.join(misc.data_dir(),'{{datastore}}'))

for year in range({{numyearstorun if numyearstorun else 1}}): 
  {% for arg in modelstorun -%}
  print "Running {{arg}}"
  import {{arg}}
  retval = {{arg}}.{{arg}}(dset,year={{startyear if startyear else 2010}}+year)
  if retval: open(os.path.join(misc.output_dir(),"{{arg}}.json"),"w").write(simplejson.dumps(retval,sort_keys=True,indent=4))
  {% endfor %} 

{% if saveoutput %}
dset.save_output(os.path.join(misc.runs_dir(),'run_%d.h5'%num))
{% endif %}
