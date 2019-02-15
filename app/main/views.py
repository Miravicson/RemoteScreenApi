from flask import render_template


from . import bp


@bp.route('/', methods=['GET', ])
def index():
    """ The main view function"""

    version = 'Version 1.0.0'
    message = "Let's get this project started !!!"

    return render_template('index.html', version=version, message=message)


@bp.route('/<int:page_number>', methods=['GET', 'POST'])
def page_detail(page_number):
    ''' view a page  detail '''

    return render_template('page.html', page_number=page_number)
