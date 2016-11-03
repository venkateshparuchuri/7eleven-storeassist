var userData = '';
$(document).ready(function() {
    userData = $.cookie('user');
    $('#js-today-date-bakery').val(moment().format("MMM Do YYYY"));
    $('#js-today-date-bakery').datetimepicker({
        minDate: moment().subtract(1, 'month').format('MM DD YYYY'),
        ignoreReadonly: true,
        format: 'MMM Do YYYY',
        maxDate: moment()
    });
    $('#js-gasDip-reportDate').val(moment().format("MMM Do YYYY"));
    $('#js-gasDip-reportDate').datetimepicker({
        minDate: moment().subtract(1, 'month').format('MM DD YYYY'),
        ignoreReadonly: true,
        format: 'MMM Do YYYY',
        maxDate: moment()
    });
    $('#js-changeOrderDate').val(moment().format("MMM Do YYYY"));
    $('#js-changeOrderDate').datetimepicker({
        minDate: moment().subtract(1, 'month').format('MM DD YYYY'),
        ignoreReadonly: true,
        format: 'MMM Do YYYY',
        maxDate: moment()
    });
    paymentReportTemplate = MyApp.templates.paymentReport;
    cardReaderTemplate = MyApp.templates.cardReaderTemp;
    reportSuccessTemp = MyApp.templates.reportSuccessTemp;
    reportErrTemplate = MyApp.templates.reportErrTemp;
    changeOrderTemp = MyApp.templates.table;
    createNewOrderTemp = MyApp.templates.createOrder;
    receivedOrderTemp = MyApp.templates.receivedOrder;
    bakeryOrderTemp = MyApp.templates.bakeryOrder;
    homeTemp = MyApp.templates.home;
    printShelfTemp = MyApp.templates.printShelfTag;
    manualGasTemp = MyApp.templates.gasDipReport;
    manualGasEntryTemp = MyApp.templates.gasDipReportEntry;
    manualGasEntryBasedOnDateTemp = MyApp.templates.dipReportInfo;
    moneyOrderTemp = MyApp.templates.moneyOrder;
    moneyOrderErrTemp = MyApp.templates.moneyOrderErr;
    moneyOrderCashedTemp = MyApp.templates.moneyOrderCashedErr;
    moneyOrderInfoTemp = MyApp.templates.moneyOrderInfo;
    moneyOrderConfirmationTemp = MyApp.templates.moneyOrderConfirmation;
    moneyOrderSuccessPopupTemp = MyApp.templates.moneyOrderSuccessTemp;
    checkInDataTemp = MyApp.templates.checkinData;
    $('#js-dynamicDataDiv').html('');
    $('#js-dynamicDataDiv').append('<div class="col-lg-offset-5 dots-loader spinner-div-style" style="margin-top:20%; margin-left: 50%">Loading…</div>');
    getNotificationData();
});

$(document).delegate('.js-statusText', 'click', function(ev) {
    ev.preventDefault();
    if ($(this).text() == 'Show') {
        $(this).parent().find("i.fa-angle-double-down").removeClass("fa-angle-double-down").addClass("fa-angle-double-up");
        $(this).text('Hide');
        var dataElement = $(this);
        var readStatus = parseInt($(this).parent().attr('data-read'));
        var message_id = parseInt($(this).parent().attr('data-message_id'));
        if (readStatus == 1) {
            $.ajax({
                type: "PUT",
                url: apiURL + "/route/bakery/message",
                data: JSON.stringify({
                    'read': 0,
                    'message_id': message_id,
                    'store_id': userData.store_id
                }),
                contentType: "application/json; charset=utf-8",
                success: function(response) {
                    $(dataElement).closest('div.bs-callout-danger').removeClass('bs-callout-danger').addClass('bs-callout-success');
                    var count = parseInt($('.js-notificationCount').text());
                    $('.js-notificationCount').text(count - 1);
                    if (count == 1) {
                        $('.js-notificationCount').closest('div').hide();
                    }
                }
            });
        }
    } else {
        $(this).parent().find("i.fa-angle-double-up").removeClass("fa-angle-double-up").addClass("fa-angle-double-down");
        $('.js-statusText').text('Show');
    }
});

function dynamicTime() {
    setInterval(function() {
        $('.js-itPaymentTime').val(moment().format('h:mm A'));
        $('.js-itPaymentDate').val(moment().format("MM/DD/YYYY"));
        $('.js-cardReaderTime').val(moment().format('h:mm A'));
        $('.js-cardReaderDate').val(moment().format("MM/DD/YYYY"));
        $('.js-createOrderDate').val(moment().format("MM/DD/YYYY"));
    }, 1000);
}

$(document).delegate('.js-side-nav li', 'click', function(ev) {
    ev.preventDefault();
    $('.js-side-nav li').removeClass('active');
    $(this).closest('li').addClass('active');
    $('.js-tabInfo').text($(this).find('a').text());
    $('#js-datepickerDiv').hide();
    $('.js-changeOrder').hide();
    $('.ui-pnotify').hide();
    $('#js-gasDipreportDiv').hide();
    $('#js-dynamicDataDiv').html('');
    $('#js-dynamicDataDiv').append('<div class="col-lg-offset-5 dots-loader spinner-div-style" style="margin-top:20%; margin-left: 50%">Loading…</div>');
    if ($(this).find('a').text() == 'IT & Payment Equipment Check Report') {
        checkTheStatusOfItPaymentCheckReport();
    } else if ($(this).find('a').text() == 'Card Reader Check Report') {
        checkTheStatusOfCardReaderCheckReport();
    } else if ($(this).find('a').text() == 'Change Orders') {
        getChangeOrderList();
    } else if ($(this).find('a').text() == 'Bakery Orders') {
        bakeryOrders();
        $('#js-datepickerDiv').show();
    } else if ($(this).find('a').text() == 'Home') {
        getNotificationData();
    } else if ($(this).find('a').text() == 'Print Shelf Tag') {
        getPrintShelfTagData();
    } else if ($(this).find('a').text() == 'Manual Gas Dip Report') {
        getManualGasDipReportData();
    } else if ($(this).find('a').text() == 'Money Order') {
        getMoneyOrderData();
    } else if ($(this).find('a').text() == 'Cash Reconciliation: Shift Check-In') {
        getCheckInData();
    } else if ($(this).find('a').text() == 'Cash Reconciliation: End of Day') {
        getEndOfTheDayData();
    } else {
        $('#js-dynamicDataDiv').html('');
    }
});

function getCheckInData() {
    var errHtml = checkInDataTemp();
    $('#js-dynamicDataDiv').html(errHtml);
    $('.js-headingText').html('Cash Reconciliation : Shift Check-In')
}

function getEndOfTheDayData() {
    var errHtml = checkInDataTemp();
    $('#js-dynamicDataDiv').html(errHtml);
    $('.js-headingText').html('Cash Reconciliation : Shift End Of The Day')
}

function getMoneyOrderData() {
    var dataHtml = moneyOrderTemp();
    $('#js-dynamicDataDiv').html(dataHtml);
    //$(window).keyup();
}

$(document).delegate('.js-moneyOrderSubmit', 'click', function(ev) {
    ev.preventDefault();
    $(this).button('loading');
    var dataObj = {};
    dataObj.SerialNo = $('.js-moneyOrderNum').val();
    dataObj.Store = userData.store_id;
    $.ajax({
        type: "POST",
        url: apiURL + "/route/moneyOrder/moneyOrderInquire",
        data: JSON.stringify(dataObj),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            if (response.status == "failure") {
                var errHtml = moneyOrderErrTemp();
                $('#js-dynamicDataDiv').html(errHtml);
            } else if (response.status == "success") {
                var data = {
                    rows: response.response,
                    number: dataObj.SerialNo
                };
                var errHtml = moneyOrderInfoTemp(data);
                $('#js-dynamicDataDiv').html(errHtml);
                $('.js-moneyOrderConfirmSubmit').attr('data-cashed', response.Cashed);
            }
        }
    });
});

$(document).delegate('.js-moneyOrderExit', 'click', function(ev) {
    ev.preventDefault();
    getMoneyOrderData();
});
$(document).delegate('.js-moneyOrderConfirmSubmit', 'click', function(ev) {
    ev.preventDefault();
    if ($(this).attr('data-cashed') == "true") {
      var errHtml = moneyOrderCashedTemp();
      $('#js-dynamicDataDiv').html(errHtml);
    } else {
      var serialNo = $('.js-moneyOrderConfirmNumber').val();
      var cnfrmHtml = moneyOrderConfirmationTemp();
      $('#js-dynamicDataDiv').html(cnfrmHtml);
      $('.js-moneyOrderCashed').attr('data-SerialNo', serialNo);
    }
});
$(document).delegate('.js-moneyOrderCashed', 'click', function(ev) {
    ev.preventDefault();
    var dataObj = {};
    dataObj.SerialNo = $('.js-moneyOrderCashed').attr('data-SerialNo');
    dataObj.Store = userData.store_id;
    $.ajax({
        type: "POST",
        url: apiURL + "/route/moneyOrder/moneyOrderCash",
        data: JSON.stringify(dataObj),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            if (response.status == "failure") {
                var errHtml = moneyOrderErrTemp();
                $('#js-dynamicDataDiv').html(errHtml);
            } else if (response.status == "success") {
                var successHtml = moneyOrderSuccessPopupTemp();
                $('#js-dynamicDataDiv').html(successHtml);
            }
        }
    });
})
$(document).delegate('.js-moneyOrderQuit', 'click', function(ev) {
    ev.preventDefault();
    getMoneyOrderData();
});
$(document).delegate('.js-moneyOrderSuccess', 'click', function(ev) {
    ev.preventDefault();
    getMoneyOrderData();
});

function getManualGasDipReportData() {
    $('#js-gasDipreportDiv').show();
    var store_id = userData.store_id;
    var date = moment($('#js-gasDip-reportDate').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
    $.ajax({
        type: "GET",
        url: apiURL + "/route/bakery/manualGasDipReport",
        data: {
            store_id: store_id,
            date: date
        },
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            var data = {
                rows: response.response,
                date: response.response[0].Date,
                init: response.response[0].init,
                dipped_yn: response.response[0].dipped_yn
            };
            var errHtml = manualGasEntryTemp(data);
            $('#js-dynamicDataDiv').html(errHtml);
        }
    });
}

$(document).delegate('.js-gasDipReportSubmit', 'click', function(ev) {
    ev.preventDefault();
    $(this).button('loading');
    var dataObj = {};
    dataObj.init = $('.js-empIntial').val();
    if ($("input[name='reportConfirmation']:checked").val() == 'true') {
        dataObj.dipped_yn = 1;
    } else {
        dataObj.dipped_yn = 0;
    }
    dataObj.reported_date = moment($('#js-gasDip-reportDate').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
    dataObj.store_id = userData.store_id;
    dataObj.status = $(this).attr('data-accType');
    dataObj.DipReport = [];
    $('.js-manualGasDipBody tr').each(function(ev) {
        var obj = {};
        obj.tank = parseInt($(this).find('p.js-tank').text());
        obj.water = parseFloat($(this).find('input.js-water').val());
        obj.status = dataObj.status;
        if (obj.water >= 0) {
            if (dataObj.dipped_yn == 1) {
                dataObj.DipReport.push(obj);
            } else {
                $('.js-gasDipReportSubmit').button('reset');
                new PNotify({
                    title: 'Failed!',
                    text: 'Please check "yes" to proceed further',
                    type: 'error',
                    styling: 'fontawesome',
                    hide: false
                });
            }
        }
    })
    if (dataObj.DipReport.length > 0) {
        $.ajax({
            type: "POST",
            url: apiURL + "/route/bakery/manualGasDipReport",
            data: JSON.stringify(dataObj),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                $('.js-gasDipReportSubmit').button('reset');
                getManualGasDipReportData();
            }
        });
    }
});

function getPrintShelfTagData() {
    var dataHtml = printShelfTemp();
    $('#js-dynamicDataDiv').html(dataHtml);
    //$(window).keyup();
}

$(window).keyup(function(ev) {
    if ($('.js-side-nav li.active a').text() == 'Print Shelf Tag') {
        console.log(ev);
        var str = "0123456789321";
        $('.js-printShelfNum').val(str);
        $('.js-printShelfSubmit').attr('disabled', false);
    }
    // else if ($('.js-side-nav li.active a').text() == 'Money Order') {
    //     console.log(ev);
    //     var str = "1254596266";
    //     $('.js-moneyOrderNum').val(str);
    //     $('.js-moneyOrderNum').attr('disabled', false);
    // }
});

$(document).delegate('.js-printShelfSubmit', 'click', function(ev) {
    ev.preventDefault();
    var str = $('.js-printShelfNum').val();
    $.ajax({
        type: "GET",
        url: apiURL + "/route/bakery/shelfTag",
        data: {
            upc: str
        },
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            console.log(response);
        }
    });
});

function getNotificationData() {
    $.ajax({
        type: "GET",
        url: apiURL + "/route/bakery/message",
        data: {
            store_id: userData.store_id
        },
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            var data = {
                rows: response.response
            };
            var count = 0;
            for (var i = 0; i < response.response.length; i++) {
                if (response.response[i].read == 1) {
                    count++;
                }
            }
            if (count == 0) {
                $('.js-notificationCount').closest('div').hide();
            } else {
                $('.js-notificationCount').html(count);
            }
            var dataHtml = homeTemp(data);
            $('#js-dynamicDataDiv').html(dataHtml);
            setTimeout(getNotificationData, 3600000);
        }
    });
}

$(document).delegate('.js-notificationBell', 'click', function(ev) {
    ev.preventDefault();
    $('.js-side-nav li').removeClass('active');
    $('#js-home').parent().addClass('active');
    $('.js-changeOrder').hide();
    $('#js-datepickerDiv').hide();
    getNotificationData();
});

function checkTheStatusOfItPaymentCheckReport() {
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.reported_date = moment().format('YYYY-MM-DD');
    $.ajax({
        type: "GET",
        url: apiURL + "/route/check/itEquipmentReport",
        data: dataObj,
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            if (response.response.length > 0) {
                var time = moment(response.response[0].time, ["h:mm A"]).format("h:mm A");
                var errHtml = reportErrTemplate();
                $('#js-dynamicDataDiv').html(errHtml);
                $('.js-respTime').text(time);
            } else {
                var paymentReportHtml = paymentReportTemplate();
                $('#js-dynamicDataDiv').html(paymentReportHtml);
                $('.js-itPaymentDate').val(moment().format("MM/DD/YYYY"));
                $('.js-itPaymentTime').val(moment().format('h:mm A'));
                dynamicTime();
            }
            $('#js-reportName').text('IT & Payment Equipment');
            $('.js-respDate').text(dataObj.reported_date);
        }
    });
}

function checkTheStatusOfCardReaderCheckReport() {
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.reported_date = moment().format('YYYY-MM-DD');
    $.ajax({
        type: "GET",
        url: apiURL + "/route/check/cardCheckReport",
        data: dataObj,
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            if (response.response.length > 0) {
                var time = moment(response.response[0].time, ["h:mm A"]).format("h:mm A");
                var errHtml = reportErrTemplate();
                $('#js-dynamicDataDiv').html(errHtml);
                $('.js-respTime').text(time);
            } else {
                var cardReaderHtml = cardReaderTemplate();
                $('#js-dynamicDataDiv').html(cardReaderHtml);
                $('.js-cardReaderDate').val(moment().format("MM/DD/YYYY"));
                $('.js-cardReaderTime').val(moment().format('h:mm A'));
                dynamicTime();
            }
            $('#js-reportName').text('Card Reader');
            $('.js-respDate').text(dataObj.reported_date);
        }
    });
}

function getChangeOrderList() {
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    $.ajax({
        type: "GET",
        url: apiURL + "/route/check/changeOrderHistory",
        data: dataObj,
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            var data = {
                rows: response.response
            };
            var tableHtml = changeOrderTemp(data);
            $('#js-dynamicDataDiv').html(tableHtml);
            $('.js-changeOrder').show();
            $('#example').DataTable({
                "pagingType": "full_numbers"
            });
            $('.dataTables_length').hide();
            $('#example_filter').remove();
        }
    });
}

$(document).delegate('input[name="reportConfirmation"]', 'change', function(ev) {
    ev.preventDefault();
    if ($(this).val() == "true") {
        $('.ui-pnotify').hide();
    }
});

$(document).delegate('.js-empIntial', 'keyup', function(ev) {
    ev.preventDefault();
    var intialValue = $.trim($('.js-empIntial').val());
    if (intialValue != '') {
        $('.ui-pnotify').hide();
    }
});

$(document).delegate('#js-itPaymentSubmit', 'click', function(ev) {
    ev.preventDefault();
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.reported_date = moment().format('YYYY-MM-DD');
    dataObj.employee_initials = $.trim($('.js-empIntial').val());
    dataObj.reported_time = moment().format('HH:MM:ss');
    if (dataObj.employee_initials != "") {
        $.ajax({
            type: "POST",
            url: apiURL + "/route/check/itEquipmentReport",
            data: JSON.stringify(dataObj),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                if (response.response.length > 0) {
                    var time = moment(response.response[0].time, ["h:mm A"]).format("h:mm A");
                    var errHtml = reportErrTemplate();
                    $('#js-dynamicDataDiv').html(errHtml);
                    $('.js-respTime').text(time);
                } else {
                    var time = moment(dataObj.reported_time, ["h:mm A"]).format("h:mm A");
                    var successHtml = reportSuccessTemp();
                    $('#js-dynamicDataDiv').html(successHtml);
                    $('.js-respTime').text(time);
                }
                $('#js-reportName').text('IT & Payment Equipment');
                $('.js-respDate').text(dataObj.reported_date);
            }
        });
    } else {
        new PNotify({
            title: 'Failed!',
            text: 'Please enter employee intials',
            type: 'error',
            styling: 'fontawesome',
            hide: false
        });
    }
});

$(document).delegate('#js-cardReaderSubmit', 'click', function(ev) {
    ev.preventDefault();
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.reported_date = moment().format('YYYY-MM-DD');
    dataObj.employee_initials = $.trim($('.js-empIntial').val());
    dataObj.reported_time = moment().format('HH:MM:ss');
    if (dataObj.employee_initials != "") {
        $.ajax({
            type: "POST",
            url: apiURL + "/route/check/cardCheckReport",
            data: JSON.stringify(dataObj),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                if (response.response.length > 0) {
                    var time = moment(response.response[0].time, ["h:mm A"]).format("h:mm A");
                    var errHtml = reportErrTemplate();
                    $('#js-dynamicDataDiv').html(errHtml);
                    $('.js-respTime').text(time);
                } else {
                    var time = moment(dataObj.reported_time, ["h:mm A"]).format("h:mm A");
                    var successHtml = reportSuccessTemp();
                    $('#js-dynamicDataDiv').html(successHtml);
                    $('.js-respTime').text(time);
                }
                $('#js-reportName').text('Card Reader');
                $('.js-respDate').text(dataObj.reported_date);
            }
        });
    } else {
        new PNotify({
            title: 'Failed!',
            text: 'Please enter employee initials',
            type: 'error',
            styling: 'fontawesome',
            hide: false
        });
    }
});

$(document).delegate('.js-addNewOrder', 'click', function(ev) {
    ev.preventDefault();
    var changeOrderID = parseInt(0);
    var total = 0;
    createOrderBasedOnOrderId(changeOrderID, total);
});

$(document).delegate('.js-order-actions', 'click', function(ev) {
    ev.preventDefault();
    $(this).button('loading');
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.orderBy = $.trim($('.js-empOrderIntial').val());
    dataObj.orderTime = moment().format('YYYY-MM-DD H:mm:ss');
    dataObj.orderStatus = $(this).attr('data-accType');
    dataObj.receivedStatus = "";
    if ($(this).attr('data-changeorderid') != "") {
        dataObj.orderID = $(this).attr('data-changeorderid');
    } else {
        dataObj.orderID = 0;
    }
    var dataArray = [];
    $('#js-createOrderBody tr').each(function() {
        var dataObj = {};
        dataObj.orderQuantity = parseFloat($(this).find('td.js-orderNumber input').val());
        dataObj.currencyId = $(this).find('td.js-orderNumber input').attr('data-currencyId');
        if ($(this).find('td.js-orderNumber input').attr('data-id') != '') {
            dataObj.changeorderId = $(this).find('td.js-orderNumber input').attr('data-id')
        } else {
            dataObj.changeorderId = 0;
        }
        if (dataObj.orderQuantity >= 0) {
            dataArray.push(dataObj);
        }
    })
    if (dataArray.length > 0) {
        dataObj.changeOrderDetails = dataArray;
        $.ajax({
            type: "POST",
            url: apiURL + "/route/check/changeOrder",
            data: JSON.stringify(dataObj),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                getChangeOrderList();
            }
        });
    } else {
        $('.js-order-actions').button('reset');
    }
});

$(document).delegate('.js-change-entry', 'keyup click blur', function(ev) {
    //$('.ui-pnotify').remove();
    var count = 0;
    if (parseInt($(this).val()) % parseInt($(this).attr('data-amount')) != 0 && $(this).val() != "") {
        $(this).parent().addClass('has-error');
        if ($('.ui-pnotify ').length < 1) {
            new PNotify({
                title: 'Failed!',
                text: 'Please enter correct value',
                type: 'error',
                styling: 'fontawesome',
                hide: false
            });
        }
    } else {
        if ($('.has-error').length < 0) {
            $('.ui-pnotify').remove();
        }
    }
    $('#js-createOrderBody tr').each(function() {
        if ($(this).find('input.js-change-entry').val() >= 0 && $(this).find('input.js-change-entry').val() != "") {
            if (parseInt($(this).find('input.js-change-entry').val()) % parseInt($(this).find('input.js-change-entry').attr('data-amount')) != 0 && parseInt($(this).find('input.js-change-entry').val()) > 0) {
                $(this).find('input').closest('tr').addClass('has-error');
            }
            count = count + parseFloat($(this).find('input.js-change-entry').val())
        }
    });
    if (count > 0) {
        $('.js-ordered-amountTotal').val(count);
    } else {
        $('.js-ordered-amountTotal').val('');
    }
});

function bakeryOrders() {
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.date = moment($('#js-today-date-bakery').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
    if (moment($('#js-today-date-bakery').val(), 'MMM Do YYYY').isSame(moment(), 'day')) {
        var status = 'today';
    } else {
        var status = 'notToday';
    }
    $.ajax({
        type: "GET",
        url: apiURL + "/route/bakery/bakeryOrders",
        data: dataObj,
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            console.log(response.response);
            var data = {
                rows: response.response,
                status: status
            };
            var bakeryHtml = bakeryOrderTemp(data);
            $('#js-dynamicDataDiv').html(bakeryHtml);

        }
    });

}

$(document).delegate('.fa-calendar', 'click', function(ev) {
    //Trigger the event on the next element.
    $(this).next().trigger('select');
});


function createOrderBasedOnOrderId(changeOrderID, total, orderedBy) {
    var dataObj = {};
    dataObj.store_id = userData.store_id;
    dataObj.date = moment().format('YYYY-MM-DD H:mm:ss');
    dataObj.changeorderId = changeOrderID;
    $.ajax({
        type: "GET",
        url: apiURL + "/route/check/changeOrder",
        data: dataObj,
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            var data = {
                denominations: response.response
            };
            data.changeOrderId = changeOrderID;
            data.ordered_by = orderedBy;
            data.total = total;
            var tempHtml = createNewOrderTemp(data);
            $('#js-dynamicDataDiv').html(tempHtml);
            dynamicTime();
            var count = 0;
            $('#js-createOrderBody tr').each(function() {
                if ($(this).find('input.js-orderPrice').val() > 0) {
                    count = count + parseFloat($(this).find('input.js-orderPrice').val())
                }
            });
            if (count > 0) {
                $('.js-orderTotal').val(count);
                $('.js-order-actions').attr('disabled', false);
            } else {
                $('.js-orderTotal').val('');
            }
        }
    });
}

$(document).delegate('.js-changeOrderActions', 'click', function(ev) {
    ev.preventDefault();
    var status = $(this).attr('data-status');
    var receivedStatus = $(this).attr('data-received_status');
    var changeOrderID = $(this).attr('data-changeOrderID');
    var orderedDate = $(this).attr('data-date');
    var orderedBy = $(this).attr('data-orderBy');
    var total = $(this).attr('data-total');
    if (status == 'Save') {
        createOrderBasedOnOrderId(changeOrderID, total, orderedBy);
    } else {
        var dataObj = {};
        dataObj.status = 'Complete';
        dataObj.changeorderId = changeOrderID;
        $.ajax({
            type: "GET",
            url: apiURL + "/route/check/changeOrderReceived",
            data: dataObj,
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                var data = {
                    denominations: response.response,
                    receivedDetails: response.response[0]
                };
                if (receivedStatus == "Complete") {
                    data.status = "Complete";
                }
                data.total = total;
                var errHtml = receivedOrderTemp(data);
                $('#js-dynamicDataDiv').html(errHtml);
                $('.js-createOrderDate').val(moment(orderedDate).format("MM/DD/YYYY"));
                $('.js-empOrderIntial').val(orderedBy);
                $('.js-receivedOrderDate').val(moment().format("MM/DD/YYYY"));
                $('.js-receiveOrder-actions').attr('data-changeOrderId', changeOrderID);
            }
        });
    }
});

$(document).delegate('.js-receivedEntry', 'click keyup blur', function(ev) {
    ev.preventDefault();
    if (parseInt($(this).val()) % parseInt($(this).attr('data-amount')) != 0 && $(this).val() != "") {
        $(this).parent().addClass('has-error');
        if ($('.ui-pnotify ').length < 1) {
            new PNotify({
                title: 'Failed!',
                text: 'Please enter correct value',
                type: 'error',
                styling: 'fontawesome',
                hide: false
            });
        }
    } else {
        if ($('.has-error').length < 0) {
            $('.ui-pnotify').remove();
        }
    }
    var receivedCount = 0;
    $('.js-receivedOrderBody tr').each(function() {
        if ($(this).find('input.js-receivedEntry').val() != "" && $(this).find('input.js-receivedEntry').val() >= 0) {
            if (parseInt($(this).find('input.js-receivedEntry').val()) % parseInt($(this).find('input.js-receivedEntry').attr('data-amount')) != 0 && parseInt($(this).find('input.js-receivedEntry').val()) > 0) {
                $(this).find('input').closest('tr').addClass('has-error');
            }
            receivedCount = receivedCount + parseFloat($(this).find('input.js-receivedEntry').val())
        }
    });
    $('.js-receivedTotal').val(receivedCount);
});

$(document).delegate('.js-receiveOrder-actions', 'click', function(ev) {
    ev.preventDefault();
    $(this).button('loading');
    var obj = {};
    var total = parseFloat($('.js-receivedOrderBody').attr('data-total'));
    if ($(this).attr('data-accType') == 'Save') {
        obj.receivedStatus = 'Save';
    } else {
        obj.receivedStatus = 'Complete';
    }
    obj.receivedBy = $('.js-receiveOrderIntial').val();
    obj.receivedDate = moment($('.js-receivedOrderDate').val()).format('YYYY-MM-DD H:mm:ss');
    obj.changeOrderID = $('.js-receiveOrder-actions').attr('data-changeOrderId');
    var receivedChangeOrder = [];
    var count = 0;
    $('.js-receivedOrderBody tr').each(function() {
        if ($(this).find('input.js-receivedEntry').val() >= 0 && $(this).find('input.js-receivedEntry').val() != '') {
            var dataObj = {};
            dataObj.receivedAmount = $(this).find('input').val();
            count = count + parseFloat($(this).find('input').val());
            if ($(this).find('td').attr('data-currencyId') == "") {
                dataObj.currencyId = 0;
            } else {
                dataObj.currencyId = $(this).find('td').attr('data-currencyId');
            }
            dataObj.currency = $(this).find('td').attr('data-currency');
            receivedChangeOrder.push(dataObj);
        }
    });
    obj.receivedChangeOrder = receivedChangeOrder;
    if (count > total) {
        $('#js-userConfirmation').modal('show');
        $('#js-user-confirmation-Yes').attr('data-obj', JSON.stringify(obj));
    } else {
        saveReceivedOrder(obj);
    }
});

$(document).delegate('#js-user-confirmation-Yes', 'click', function(ev) {
    ev.preventDefault();
    $('#js-userConfirmation').modal('hide');
    saveReceivedOrder(JSON.parse($(this).attr('data-obj')));
});

$(document).delegate('#js-user-confirmation-no', 'click', function(ev) {
    ev.preventDefault();
    $('.js-receiveOrder-actions').button('reset');
});

function saveReceivedOrder(obj) {
    $.ajax({
        type: "POST",
        url: apiURL + "/route/check/changeOrderReceived",
        data: JSON.stringify(obj),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            getChangeOrderList();
        }
    });
}

$(document).delegate('.js-bakeryOrder-actions', 'click', function(ev) {
    ev.preventDefault();
    $(this).button('loading');
    var dataArray = [];
    var status = $(this).attr('data-accType');
    $('.js-bakeryOrdersBody tr').each(function() {
        if ($(this).find('td input:disabled').length == 0) {
            var dataObj = {};
            dataObj.store_id = userData.store_id;
            dataObj.active = status;
            dataObj.date = moment($('#js-today-date-bakery').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
            dataObj.descr = $(this).attr('data-name')
            if ($(this).attr('data-requests_id') != '' && $(this).attr('data-requests_id') > 0) {
                dataObj.order_id = $(this).attr('data-requests_id');
                dataObj.last_modified = moment($('#js-today-date-bakery').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
            } else {
                dataObj.order_id = 0;
            }
            dataObj.id = $(this).attr('data-id');
            dataObj.nbr = $(this).attr('data-nbr');
            dataObj.pick_nbr = $(this).attr('data-pick_nbr');
            dataObj.sku = $(this).attr('data-sku');
            if ($(this).find('input.js-productQtyOnHand').val() != '' && $(this).find('input.js-productQtyOnHand').val() >= 0) {
                dataObj.on_hand_qty = parseInt($(this).find('input.js-productQtyOnHand').val());
            } else {
                dataObj.on_hand_qty = "null"
            }
            if ($(this).find('input.js-productQtyReturn').val() != '' && $(this).find('input.js-productQtyReturn').val() >= 0) {
                dataObj.return_qty = parseInt($(this).find('input.js-productQtyReturn').val());
            } else {
                dataObj.return_qty = "null"
            }
            if (dataObj.on_hand_qty != "null" || dataObj.return_qty != "null") {
                if (dataObj.on_hand_qty >= 0 || dataObj.return_qty >= 0) {
                    if (dataObj.on_hand_qty >= 0 && dataObj.return_qty >= 0) {

                    } else if (dataObj.on_hand_qty == "null" && dataObj.return_qty >= 0) {
                        dataObj.on_hand_qty = 0;
                    } else if (dataObj.on_hand_qty >= 0 && dataObj.return_qty == "null") {
                        dataObj.return_qty = 0;
                    }
                    dataArray.push(dataObj);
                }
            } else {
                if (dataObj.order_id > 0 && dataObj.on_hand_qty == "null" && dataObj.return_qty == "null") {
                    dataArray.push(dataObj);
                }
            }
        }
    });
    if (dataArray.length > 0) {
        $.ajax({
            type: "POST",
            url: apiURL + "/route/bakery/bakeryOrders",
            data: JSON.stringify(dataArray),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                $('.js-bakeryOrder-actions').button('reset');
                bakeryOrders();
            }
        });
    } else {
        $('.js-bakeryOrder-actions').button('reset');
    }
});

$('#js-today-date-bakery').on('dp.change', function(ev) {
    ev.preventDefault();
    if ($('.js-side-nav li.active').find('a').text() == 'Bakery Orders') {
        bakeryOrders();
    }
});
$('#js-gasDip-reportDate').on('dp.change', function(ev) {
    ev.preventDefault();
    $('#js-dynamicDataDiv').html('');
    $('#js-dynamicDataDiv').append('<div class="col-lg-offset-5 dots-loader spinner-div-style" style="margin-top:20%; margin-left: 50%">Loading…</div>');
    if ($('.js-side-nav li.active').find('a').text() == 'Manual Gas Dip Report') {
      if (moment($('#js-gasDip-reportDate').val(), 'MMM Do YYYY').isSame(moment(), 'day')) {
        getManualGasDipReportData();
      } else {
        $('#js-gasDipreportDiv').show();
        var store_id = userData.store_id;
        var date = moment($('#js-gasDip-reportDate').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
        $.ajax({
            type: "GET",
            url: apiURL + "/route/bakery/dipReportByDate",
            data: {
                store_id: store_id,
                date: date
            },
            contentType: "application/json; charset=utf-8",
            success: function(response) {
              if (response.response.length > 0) {
                var data = {
                    rows: response.response,
                    date: response.response[0].Date,
                    init: response.response[0].init,
                    dipped_yn: response.response[0].dipped_yn
                };
                var errHtml = manualGasEntryBasedOnDateTemp(data);
                $('#js-dynamicDataDiv').html(errHtml);
              } else {
                $('#js-dynamicDataDiv').html('<h4><p>There is no data available</p></h4>');
              }
            }
        });
      }
    }
});
$('#js-changeOrderDate').on('dp.change', function(ev) {
    ev.preventDefault();
    if ($('.js-side-nav li.active').find('a').text() == 'Change Orders') {
        var dataObj = {};
        dataObj.store_id = userData.store_id;
        dataObj.date = moment($('#js-changeOrderDate').val(), 'MMM Do YYYY').format('YYYY-MM-DD');
        $.ajax({
            type: "POST",
            url: apiURL + "/route/check/changeOrderHistory",
            data: JSON.stringify(dataObj),
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                var data = {
                    rows: response.response
                };
                var tableHtml = changeOrderTemp(data);
                $('#js-dynamicDataDiv').html(tableHtml);
                $('#example').DataTable({
                    "pagingType": "full_numbers"
                });
                $('.dataTables_length').hide();
                $('#example_filter').remove();
                $('#js-changeOrderDate').val(moment(dataObj.date).format("MMM Do YYYY"));
                $('#js-changeOrderDate').datetimepicker({
                    minDate: moment().subtract(1, 'month').format('MM DD YYYY'),
                    ignoreReadonly: true,
                    format: 'MMM Do YYYY',
                    maxDate: moment()
                });
            }
        });
    }
});
