from flask import render_template, url_for, flash, redirect, request, abort, send_file
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, EditProfileForm, CreateProjectForm, UpdateProjectForm
from flaskblog.models import User, Details, Projects, Intrested
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flaskblog import randomstring
from country_list import countries_for_language
import sqlite3 as sql
import requests
from io import BytesIO
from fpdf import FPDF

mail= Mail(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        uniqueid = randomstring.loginstr(form.profession.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, collegeid=form.collegeid.data, profession=form.profession.data, userloginid=uniqueid)
        db.session.add(user)
        db.session.commit()
        msg = Message('Hello', sender = 'mohanaswin6655@gmail.com', recipients = [form.email.data])
        msg.body = "Hello your account has been created! Your user name is:"+uniqueid+ ". You can login using this username and the password you have given while creating you account."
        mail.send(msg)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userloginid=form.userloginid.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check userloginid and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        msg = Message('Password Reset Request', sender = 'mohanaswin6655@gmail.com', recipients = [form.email.data])
        msg.body = f'''to reset your password click on the link below :
        {url_for('reset_token', token = token, _external = True)}

        If you did not make this request then simpley ignore this email and no changes will be made.
        '''
        mail.send(msg)
        flash('To reset you password goto your mail and follow the instructions', 'success')
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/editprofile", methods=['GET', 'POST'])
def editprofile():
    form = EditProfileForm()
    countries = dict(countries_for_language('en'))
    dropdown_list1 = ['Computing', 'Electrical', 'Megatronics', 'Electronics', 'Software Engineering']
    dropdown_list2 = ['M.Sc', 'B.Sc', 'B.Hon', 'B.Tech', 'Pg.Dip']
    dropdown_list3 = countries.values()
    return render_template('editprofile.html', title='EditProfile', form=form, dropdown_list1=dropdown_list1, dropdown_list2=dropdown_list2, dropdown_list3=dropdown_list3)

@app.route("/updateprofile", methods=['GET', 'POST'])
def updateprofile():
    form = EditProfileForm()
    userloginid = current_user.userloginid
    gender = request.form['gender']
    course = request.form['drop_course']
    degree = request.form['drop_degree']
    country = request.form['drop_country']
    intrest1 = form.intrest1.data
    intrest2 = form.intrest2.data
    intrest3 = form.intrest3.data
    intrest4 = form.intrest4.data
    intrest5 = form.intrest5.data
    lnkdurl = form.lnkdurl.data
    ghuburl = form.ghuburl.data
    conn=sql.connect("flaskblog/site.db")
    stmt = "select * from details where userloginid =\""+str(userloginid)+"\""
    cur = conn.cursor()
    cur.execute(stmt)
    data = cur.fetchall()
    print(len(data))
    if len(data) != 0:
        print(data[0][6])
        #query = "UPDATE details SET gender =\""+str(gender)+"\", course=\""+str(course)+"\", degree=\""+str(degree)+"\", country=\""+str(country)+"\", intrest1=\""+str(intrest1)+"\", intrest2=\""+str(intrest2)+"\", intrest3=\""+str(intrest3)+"\", intrest4=\""+str(intrest4)+"\", intrest5=\""+str(intrest5)+"\", lnkdurl=\""+str(lnkdurl)+"\", ghuburl=\""+str(ghuburl)+"\" Where userloginid=\""+str(userloginid)+"\""

        if data[0][3] != "":
            if gender == "":
                print("nothing to update")
            else:
                if str(data[0][3]) != gender :
                    query = "UPDATE details SET gender=\""+str(gender)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :
            query = "UPDATE details SET gender=\""+str(gender)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)


        if data[0][3] != "":
            if course == "":
                print("nothing to update")
            else:
                if str(data[0][6]) != course :
                    query = "UPDATE details SET course=\""+str(course)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :
            query = "UPDATE details SET course=\""+str(course)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][4] != "":
            if degree == "":
                print("nothing to update")
            else:
                if str(data[0][4]) != degree :
                    query = "UPDATE details SET degree=\""+str(degree)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET degree=\""+str(degree)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][5] != "":
            if country == "":
                print("nothing to update")
            else:
                if str(data[0][5]) != country :
                    query = "UPDATE details SET country=\""+str(country)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET country=\""+str(country)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][6] != "":
            if intrest1 == "":
                print("nothing to update")
            else:
                if str(data[0][6]) != intrest1 :
                    query = "UPDATE details SET intrest1=\""+str(intrest1)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET intrest1=\""+str(intrest1)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][7] != "":
            if intrest2 == "":
                print("nothing to update")
            else:
                if str(data[0][7]) != intrest2 :
                    query = "UPDATE details SET intrest1=\""+str(intrest2)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET intrest2=\""+str(intrest2)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][8] != "":
            if intrest3 == "":
                print("nothing to update")
            else:
                if str(data[0][8]) != intrest3 :
                    query = "UPDATE details SET intrest3=\""+str(intrest3)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET intrest3=\""+str(intrest3)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][9] != "":
            if intrest4 == "":
                print("nothing to update")
            else:
                if str(data[0][9]) != intrest4 :
                    query = "UPDATE details SET intrest4=\""+str(intrest4)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET intrest4=\""+str(intrest4)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][10] != "":
            if intrest5 == "":
                print("nothing to update")
            else:
                if str(data[0][10]) != intrest5 :
                    query = "UPDATE details SET intrest5=\""+str(intrest5)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET intrest5=\""+str(intrest5)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][11] != "":
            if lnkdurl == "":
                print("nothing to update")
            else:
                if str(data[0][11]) != lnkdurl :
                    query = "UPDATE details SET lnkdurl=\""+str(lnkdurl)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET lnkdurl=\""+str(lnkdurl)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)

        if data[0][12] != "":
            if ghuburl == "":
                print("nothing to update")
            else:
                if str(data[0][12]) != ghuburl :
                    query = "UPDATE details SET ghuburl=\""+str(ghuburl)+"\" Where userloginid=\""+str(userloginid)+"\""
                    conn.execute(query)
        else :    
            query = "UPDATE details SET ghuburl=\""+str(ghuburl)+"\" Where userloginid=\""+str(userloginid)+"\""
            conn.execute(query)
    else :
        print("Data Inserted")
        print("Inserted sucessfully")
        conn.execute("INSERT INTO details (userloginid,gender,course,degree,country,intrest1,intrest2,intrest3,intrest4,intrest5,lnkdurl,ghuburl) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ",(userloginid,gender,course,degree,country,intrest1,intrest2,intrest3,intrest4,intrest5,lnkdurl,ghuburl))
    print("before commit")
    conn.commit()
    conn.close()
    msg="Record Successfully added"
    return render_template('account.html', title='account')


@app.route("/proposeaproject", methods=['GET', 'POST'])
def proposeaproject():
    form = CreateProjectForm()
    return render_template('proposeaproject.html', title='Propose-a-Project', form=form)

@app.route("/createproject", methods=['GET', 'POST'])
def createproject():
    form = CreateProjectForm()
    file = request.files['inputFile']
    newFile = Projects(userloginid = current_user.userloginid, projecttitle = form.projecttitle.data, pmetadata = form.pmetadata.data, pdescription = form.pdescription.data, name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()
    print( 'record added sucessfully')
    return render_template('account.html', title='Propose-a-Project', form=form, legend='New Project')

@app.route("/myprojects", methods=['GET', 'POST'])
def myprojects():
    page = request.args.get('page', 1, type=int)
    projects = Projects.query.filter_by(userloginid=current_user.userloginid).paginate(page=page, per_page=4)
    return render_template('myprojects.html', title='My-Projects', projects=projects)

@app.route("/userproject/<int:project_id>")
def userproject(project_id):
    project = Projects.query.get_or_404(project_id)
    return render_template('userproject.html', title='project.title', project=project)

@app.route("/userproject/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def updateproject(project_id):
    project = Projects.query.get_or_404(project_id)
    if project.userloginid != current_user.userloginid:
        abort(403)
    form = UpdateProjectForm()
    if request.method == 'POST':
        project.projecttitle = form.projecttitle.data
        project.pmetadata = form.pmetadata.data
        project.pdescription = form.pdescription.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('myprojects', project_id=project_id))
    elif request.method == 'GET':
        form.projecttitle.data = project.projecttitle
        form.pmetadata.data = project.pmetadata
        form.pdescription.data = project.pdescription
    return render_template('updateproject.html', title='project.title', form=form)

@app.route("/userproject/<int:project_id>/delete", methods=['POST'])
@login_required
def deleteproject(project_id):
    project = Projects.query.get_or_404(project_id)
    if project.userloginid != current_user.userloginid:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('myprojects'))


@app.route("/userproject/<int:project_id>/download", methods=['GET'])
def downloadproject(project_id):
    project = Projects.query.get_or_404(project_id)
    file_data = Projects.query.filter_by(id=project_id).first()
    return send_file(BytesIO(file_data.data),mimetype='txt/pdf/jpeg/png', attachment_filename=file_data.name, as_attachment=True)

@app.route("/allprojects", methods=['GET', 'POST'])
def allprojects():
    page = request.args.get('page', 1, type=int)
    projects = Projects.query.paginate(page=page, per_page=4)
    return render_template('allprojects.html', title='Projects', projects=projects)

@app.route("/userproject/<int:project_id>/intrested", methods=['GET', 'POST'])
def intrest(project_id):
    project = Projects.query.get_or_404(project_id)
    intrest = Intrested(userloginid=current_user.userloginid, projectid=project_id, intrestflag=1)
    db.session.add(intrest)
    db.session.commit()
    flash('Your project has been instrested!', 'success')
    return redirect(url_for('allprojects', project_id=project_id))
