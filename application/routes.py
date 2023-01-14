
from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import DeviceDataForm, RuleDataForm, DeviceEditForm
from application.models import Device
from application.models import Rule
from application.models import Log
from datetime import datetime

@app.route("/")
def index():
    entries = Rule.query.all()
    entries_log = Log.query.all()
    for x in range(len(entries_log)):
        entries_log[x].timestamp=datetime.fromtimestamp(entries_log[x].timestamp)
    return render_template('index.html', entries=entries,entries_log=entries_log)

@app.route("/list_of_devices")
def list_of_devices():
    entries = Device.query.all()
    return render_template('list_of_devices.html', entries=entries)

@app.route("/add_device", methods=["GET","POST"])
def add_device():
    form=DeviceDataForm()
    if form.validate_on_submit():
        entry=Device(device_mac=form.device_mac.data, device_ip=form.device_ip.data, name=form.name.data)
        old_device= Device.query.filter_by(device_mac=entry.device_mac).count()
        if old_device > 0:
            flash("Incorrect data! The device with this MAC already exists ", 'danger')
        else:
            db.session.add(entry)
            db.session.commit()
            flash("Successful submission", 'success')
            return redirect(url_for('index'))
    return render_template("add_device.html", form=form)

@app.route("/edit_device/<string:entry_mac>", methods=["GET","POST"])
def edit_device(entry_mac):
    form=DeviceEditForm()
    entry = Device.query.get_or_404(entry_mac)

    if form.validate_on_submit():
        entry.name = form.edit_name.data

        db.session.commit()
        flash("Successful edit", 'success')
        return redirect(url_for('list_of_devices'))
    return render_template('edit_device.html', entry=entry, form=form)

@app.route("/add_rule", methods=["GET","POST"])
def add_rule():
    form=RuleDataForm()

    if form.validate_on_submit():
        entry=Rule(card_id=form.card_id.data, reader_mac=str(form.reader_mac.data), door_mac=str(form.door_mac.data))
        entry.reader_mac=entry.reader_mac[8:]
        entry.reader_mac = entry.reader_mac[:-1]
        entry.door_mac = entry.door_mac[8:]
        entry.door_mac = entry.door_mac[:-1]
        db.session.add(entry)
        db.session.commit()
        flash("Successful submission", 'success')
        return redirect(url_for('index'))
    return render_template("add_rule.html", form=form)

@app.route('/delete_rule/<int:entry_id>')
def delete_rule(entry_id):
    entry=Rule.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was success", 'success')
    return redirect(url_for("index"))

@app.route('/delete_log/<int:entry_log_id>')
def delete_log(entry_log_id):
    entry=Log.query.get_or_404(int(entry_log_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was success", 'success')
    return redirect(url_for("index"))

@app.route('/delete_device/<entry_id>')
def delete_device(entry_id):
    entry=Device.query.get_or_404(entry_id)
    old_rule_reader = Rule.query.filter_by(reader_mac=entry.device_mac).count()
    old_rule_door = Rule.query.filter_by(door_mac=entry.device_mac).count()
    old_log=Log.query.filter_by(reader_mac=entry.device_mac).count()
    if old_rule_reader > 0 :
        Rule.query.filter_by(reader_mac=entry.device_mac).delete()


    if old_rule_door > 0 :
        Rule.query.filter_by(door_mac=entry.device_mac).delete()

    if old_log > 0 :
        Log.query.filter_by(reader_mac=entry.device_mac).delete()




    db.session.delete(entry)
    db.session.commit()
    flash("Successful deletion", 'success')
    return redirect(url_for("list_of_devices"))
