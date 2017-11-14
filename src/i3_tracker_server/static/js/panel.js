var selected = '';

function datepickerShift(offset)
{
    datepicker = document.getElementById('datepicker');
    date = $.datepicker.parseDate($.datepicker.COOKIE, datepicker.value);
    date.setDate(date.getDate() + offset);
    $('#datepicker').datepicker('setDate', date);
}

function updateSelection()
{
    var e = document.getElementById('windowClassSelection');
    var newSelected = e.options[e.selectedIndex].value;

    document.getElementById('svg_' + selected).style = 'display: none;';
    document.getElementById('svg_' + newSelected).style = 'display: block';

    selected = newSelected;
}

function onResize()
{
var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

    //X = document.body.clientWidth;
    //Y = document.body.clientHeight;
    let X = x;
    let Y = y;

    console.log(X, Y);

    let topY = document.getElementById('top').clientHeight;
    let bottomY = Y - topY;

    document.getElementById('bottom').style.height = bottomY + 'px';
    document.getElementById('bottom_table').style.height = bottomY + 'px';
    document.getElementById('bottom_row').style.height = bottomY + 'px';
    document.getElementById('bottom_left').style.height = bottomY + 'px';
    document.getElementById('bottom_right').style.height = bottomY + 'px';

    console.log(topY, bottomY);

    let bottomTopY = document.getElementById('bottom_header').clientHeight;
    let bottomBodyY = bottomY - bottomTopY;

    document.getElementById('IDtable').style.height = bottomBodyY + 'px';
    console.log(topY, bottomTopY, bottomBodyY);
    //document.getElementById('IDtable').style.setAttribute('overflow-y', 'scroll');
    $('#IDtable').css({"height": bottomBodyY + "px", "overflow-y": "scroll"});
//        document.getElementById(avatar).style.height = B + 'px';
//        document.getElementById(avatar + "_img").style.width = B + 'px';
    console.log("x");
}

function changeDate()
{
    let value = document.getElementById('datepicker').value;
    let date = $.datepicker.parseDate($.datepicker.COOKIE, value);

/*            console.log(date);
            console.log(date.getFullYear());
            console.log(date.getMonth()+1);
            console.log(date.getDate());
*/
    document.location = 'http://tracker/panel/' + date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate() + '/';
}

function bootstrap(year, month, day)
{
    document.getElementById('svg_').style = 'display: block;';

    $( "#datepicker" ).datepicker({
        showOn: "button",
        buttonImageOnly: false,
        buttonText: "Calendar",
        dateFormat: $.datepicker.COOKIE,
        onSelect: function(dateText) {
            changeDate();
        }
    });
    $('#datepicker').datepicker('setDate', $.datepicker.parseDate('yy-mm-dd', year+'-'+month+'-'+day));

    (Array.from(document.body.getElementsByTagName('a'))).forEach(function(domElement){
                let link = domElement.getAttribute('xlink:href');
                if (link) {
                let id_hash = link.slice(1);
                domElement.removeAttribute('target');
                domElement.addEventListener('mouseover', function() {
                    let sourceDom = document.getElementById(id_hash);
                    let targetDom = document.getElementById('highlight');
                    targetDom.innerHTML = sourceDom.innerHTML;
                });
                domElement.addEventListener('mouseout', function() {
                    let sourceDom = document.getElementById('emptyHighlight');
                    let targetDom = document.getElementById('highlight');
                    targetDom.innerHTML = sourceDom.innerHTML;
                });
                } else {
                //console.log(domElement);
                }
            });

    $("#sortable").tablesorter({});

    $top_table = $("#IDtable").tablesorter({
        widgets: ['zebra', 'filter'],
        widgetOptions: {
            filter_columnFilters: false,
            filter_searchDelay: 100,
            // include child row content while filtering, if true
            filter_childRows  : false,
            // class name applied to filter row and each input
            filter_cssFilter  : 'tablesorter-filter',
            // search from beginning
            filter_startsWith : false,
            // Set this option to false to make the searches case sensitive
            filter_ignoreCase : true
        }
    });

    $.tablesorter.filter.bindSearch( $top_table, $('.search') );
    $('#search').trigger('keyup', []);
    $.tablesorter.filter.value = $('#search').value;

    onResize();
}

