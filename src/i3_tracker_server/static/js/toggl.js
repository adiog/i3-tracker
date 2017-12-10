function server_load()
{
    console.log('server_load');
}

function server_save()
{
    console.log('server_save');
}

function local_storage_load()
{
    console.log('server_load');
}

function local_storage_save()
{

}

class ResetButton {
    constructor(cb) {
        this.dom = img({class: "imgButton", width: "64px", height: "64px", src: '/static/img/breakpoints.png'});
        this.dom.addEventListener('click', cb);
    }
}

const TOGGL_RECORDING = {
    'OFF': 0,
    'ON': 1
}

class ToggleButton
{
    constructor(cb)
    {
        let that = this;
        this.cb = cb;
        this.dom = img({width: "64px", height: "64px"});
        this.dom.addEventListener('click', function(){ that.toggle(); });
        this.setStopped();
    }

    setRunning()
    {
        this.toggleFlag = TOGGL_RECORDING.ON;
        this.dom.src = '/static/img/media_stop.png';
        this.dom.className = 'imgButton pulse';
    }

    setStopped()
    {
        this.toggleFlag = TOGGL_RECORDING.OFF;
        this.dom.src = '/static/img/media_record.png';
        this.dom.className = 'imgButton nonpulse';
    }

    toggle()
    {
        if (this.toggleFlag === TOGGL_RECORDING.ON)
        {
            this.setStopped();
        }
        else
        {
            this.setRunning();
        }
        this.cb();
    }
}

function zpad(n)
{
    return (n+"").padStart(2,"0");
}

function format_seconds(seconds)
{
    hours = Math.floor(seconds / 3600);
    seconds = seconds - hours * 3600;
    minutes = Math.floor(seconds / 60);
    seconds = seconds - minutes * 60;
    return zpad(hours) + ':' + zpad(minutes) + ':' + zpad(seconds);
}


class MainLineView
{
    constructor() {
        let that = this;
        this.pk = null;
        this.range_start = null;
        //this.isRunning = false;
        //this.seconds = 0;
        //this.timepoints = [];
        this.resetButton = new ResetButton(function(){that.reset();});
        this.toggleButton = new ToggleButton(function(){that.toggle();});
        this.dom = $$(table({id: 'togglMainLine', style: "margin: auto; height: 80px; width: 80%; border: 1px solid black; clear: both;"}),
            $$(tr(),
                $$(td({style: "width: 10%;"}), this.resetDom = this.resetButton.dom),
                $$(td({style: "width: 70%;"}), this.text = textarea({style: "width: 100%; font-size: 2.0em;"})),
                $$(td({style: "width: 10%;"}), this.time = span()),
                $$(td({style: "width: 10%;"}), this.toggleDom = this.toggleButton.dom)
            )
        );
        this.text.addEventListener('keypress', function(event){return that.onKeyPressed(event);});
        this.resetTime();
        this.running();
    }

    toggle_running()
    {
        if (this.isRunning) {
            console.log('stopping..');
            this.stop();
        } else {
            if (this.seconds === 0) {
                console.log('starting..');
                this.start();
            } else {
                console.log('resuming..');
                this.resume();
            }
        }
    }

    onKeyPressed(event) {
        let key = event.keyCode;

        if (key === 13) {
            event.preventDefault();
            this.toggle_running();
//            document.getElementById("txtArea").value = document.getElementById("txtArea").value + "\n*";
            return false;
        }
        else {
            return true;
        }
    }

    create_task() {
        let that = this;
        GetJSON('/toggl/create/task/', {name: this.text.value}, function(data) {console.log(data);that.pk = data.pk;});
        console.log('this.create_task()');
        console.log(this.pk);
    }

    start() {
        this.resetTime();
        this.create_task();
        this.resume();
    }

    resume()
    {
        this.isRunning = true;
        this.toggleButton.setRunning();
        this.registerTimepoint();
    }

    stop()
    {
        this.isRunning = false;
        this.toggleButton.setStopped();
        this.registerTimepoint()
    }

    registerTimepoint()
    {
        let now = Date.now();
        if (this.range_start === null) {
            this.range_start = now;
        } else {
            GetJSON('/toggl/create/range/', {pk: this.pk, start: this.range_start, stop: now}, function(resp){console.log(resp);});
            this.range_start = null;
        }
        this.timepoints.push(now);
        console.log(this.timepoints);
    }

    resetActivity()
    {
        this.resetName();
        this.resetTime();
    }

    resetName() {
        this.text.value = '';
    }

    resetTime(){
        this.isRunning = false;
        this.timepoints = [];
        this.seconds = 0;
        this.time.innerHTML = format_seconds(this.seconds); //'not yet started';

    }

    store()
    {
        if (this.seconds !== 0 || this.text.value !== '') {
            console.log('Task [' + this.text.value + '] done.');
            console.log(this.timepoints);
            tbody = document.getElementById('togglTbody');
            tbody.appendChild(
                $$(tr(),
                    $$$(td(), this.text.value),
                    $$$(td(), this.timepoints[0]),
                    $$$(td(), this.timepoints[this.timepoints.length - 1]),
                    $$$(td(), format_seconds(this.seconds))
                )
            );
        }
    }

    reset(){
        this.stop();
        this.store();
        this.resetActivity();
    }

    toggle()
    {
        this.toggle_running();
        console.log('event');
    }

    running()
    {
        let that = this;
        console.log('heartbeat');
        if (this.isRunning) {
            this.seconds = this.seconds + 1;
            this.time.innerHTML = format_seconds(this.seconds);
            console.log('Task [' + this.text.value + '] is working for total ' + this.seconds + ' seconds...');
        }
        setTimeout(function(){that.running();}, 1000);
    }
}

class MainLine
{

}


class TableLine {
    draw() {
        //button reset
        //label
        //button start/stop
    }

}

class Table {

}


function draw_table() {

}

const TOGGL = {
    'OFF': 0,
    'ON': 1
};


class TogglController
{
    constructor()
    {
        this.logo = document.getElementById('logo');
        this.togglComponent = document.getElementById('togglComponent');
        this.togglLine = document.getElementById('togglLine');
        this.togglTable = document.getElementById('togglTable');
        this.dom = div();
        this.mainlineview = new MainLineView();
        this.togglLine.appendChild(this.mainlineview.dom);
        this.togglComponent.style.display = 'none';
        this.togglTable.style.display = 'none';
        this.mode = TOGGL.OFF;
        this.make_logo_toggle();
    }

    make_logo_toggle()
    {
        let that = this;
        this.logo.addEventListener('click', function(){ that.toggleLogo(); });
    }

    toggleLogo()
    {
        this.mode = (this.mode === TOGGL.OFF) ? TOGGL.ON : TOGGL.OFF;
        if (this.mode === TOGGL.ON) {
            this.logo.src = '/static/img/hourglass.png';
            this.togglComponent.style.display = 'inline';
            this.togglTable.style.display = 'inline';
        }
        else {
            this.logo.src = '/static/img/icon.png';
            this.togglComponent.style.display = 'none';
            this.togglTable.style.display = 'none';
        }
    }
}

