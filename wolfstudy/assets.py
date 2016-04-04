from flask.ext.assets import Bundle

# Initialize flask assets
common_css = Bundle(
    'less/main.less',
    filters='less,cssmin', 
    output='css/common.css'
)