# IPython log file

from isp_final import Object
import flaskr
flaskr.session.query(Object).all()[0]
flaskr.session.query(Object).all()[0].to_json()
startlog
get_ipython().magic(u'logstart ')
