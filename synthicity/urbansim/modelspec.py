{% macro IMPORTS() %}
import pandas as pd, numpy as np, statsmodels.api as sm
from synthicity.urbanchoice import *
from synthicity.utils import misc
import time, copy, os, sys
from patsy import dmatrix
{% endmacro %}

{% macro TABLE(tblname) %}
{% if not template_mode == "estimate" and table_sim %}
{{tblname}} = {{table_sim}}
{% else %}
{{tblname}} = {{table}}
{% endif %}
{% if filters %}
{% for filter in filters %}
{{tblname}} = {{tblname}}[{{filter|replace("_tbl_",tblname)}}]
{% endfor %}
{% endif %}
{% if template_mode == "estimate" and estimate_filters %}
{% for filter in estimate_filters %}
{{tblname}} = {{tblname}}[{{filter|replace("_tbl_",tblname)}}]
{% endfor %}
{% endif %}
{% if not template_mode == "estimate" and simulate_filters %}
{% for filter in simulate_filters %}
{{tblname}} = {{tblname}}[{{filter|replace("_tbl_",tblname)}}]
{% endfor %}
{% endif %}
{% endmacro %}
  
{% macro MERGE(tablename,merged) %} 
t_m = time.time()
{{tablename}} = pd.merge({{tablename}},{{merged.table}},**{{merged|droptable}})
print "Finished with merge in %f" % (time.time()-t_m)
{% endmacro %}

{% macro CALCVAR(table,varname,var_lib) %}
{% if varname in var_lib %}
({{var_lib[varname]|replace("_tbl_",table)}}).astype('float')
{% else %}
{{table}}["{{varname}}"]
{% endif %}
{% endmacro %}

{% macro SPEC(inname,outname,submodel=None,newdf=True) %} 
{%- if patsy %}
print "WARNING: using patsy, ind_vars will be ignored"
{{outname}} = dmatrix("{{patsy}}", data={{inname}}, return_type='dataframe')
{% else -%}
{% if newdf %}
{{outname}} = pd.DataFrame(index={{inname}}.index)
{% else -%}
{{outname}} = {{inname}}
{% endif %}
if 0: pass
{% if submodel_vars %}
{% for k, v in submodel_vars.iteritems() %}
elif {{submodel}} == "{{k}}":
{% for varname in v %}
  {{outname}}["{{varname}}"] = {{CALCVAR(inname,varname,var_lib)-}}
{% endfor %}
{% endfor %}
{% endif %}
else:
{% for varname in ind_vars %}
  {{outname}}["{{varname}}"] = {{CALCVAR(inname,varname,var_lib)-}}
{% endfor %}
{% if add_constant %}
{{outname}} = sm.add_constant({{outname}},prepend=False)
{% endif %}
{{outname}} = {{outname}}.fillna(0)
{% endif -%}
{% endmacro %}
