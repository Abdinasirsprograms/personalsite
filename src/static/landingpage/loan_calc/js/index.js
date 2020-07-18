var principle, apr, term, paymentSchedule, displayChart;
var notBlank = false;
function convertToTwoDecimalSpots(number){
    return Number((Math.round(number * 100)/100).toFixed(2));
}
// Amortized loan
// Payment = Amount / Discount Facor
function payments(Principle, DiscountFactor){
    return convertToTwoDecimalSpots(Principle/DiscountFactor)
}
// n = # of payments per year * loan term length
function paymentsPerYear(termLength) {
    let paymentPeriods = Math.round(termLength) * 12;
    return paymentPeriods;
}
// r = APR/12
function periodicInterestRate(APR) {
    let rate = Number((parseFloat(APR)/100).toFixed(2));
    return rate/12;
}
// D = {[(1 + r)n] - 1}/[r(1 + r)n]
function discountFactor(rate, paymentPeriod){
    let paymentPeriods = Math.round(paymentPeriod);
    let rateAddOne = rate + 1;
    let rateMulitpliedByPaymentPeriods = rateAddOne ** paymentPeriods;
    let DiscountFactor = (rateMulitpliedByPaymentPeriods - 1)/(rate * rateMulitpliedByPaymentPeriods);
    return DiscountFactor;
}
// Payments for just interest
// Payment = Amount * (APR/12)
function interestOnly(loanAmount, APR){
    let YearlyAPR =  ((parseFloat(APR)/100))/12;
    let Payments = Number((loanAmount * YearlyAPR).toFixed(2));
    return Payments
}
// example: loan of 10k at 3% for 7 years
// n = 84 (12 monthly payments/year * 7 years)
// r = 0.0025 (0.03/by 12 payments per year)
// D = 75.6813 {[(1+0.0025)84] - 1} / [0.0025(1+0.0025)84]
// P = $132.13 (10,000/75.6813)
// calculating the interest only payment on the above example:
// Payment = Amount * (APR/12)
// P = $25 (10,000 * (0.03/12))

function listen_for_input(e) {
    switch(e.target.name){
        case 'term':
            term = parseFloat(e.target.value);
            break;
        case 'principle':
            principle = parseInt(e.target.value);
            break;
        case 'apr':
            apr = parseFloat(e.target.value);
            break;
        default:
            console.log('None')
            break;
    }
    if((!term) || (!principle) || (!apr)){
        notBlank = true;
    }
    else {
        notBlank = false;
    }
    var returnPaymentSchedule = amortizedLoan();
    if(displayChart && returnPaymentSchedule){
        displayChart.destroy()
        displayChart = chartData(returnPaymentSchedule);
        document.querySelector("#chart").style.display = "block";
    }
    else if (returnPaymentSchedule) {
        displayChart = chartData(returnPaymentSchedule);
        document.querySelector("#chart").style.display = "block";
    }
    return 
}

document.querySelector("input[name=principle]").addEventListener('input', listen_for_input);
document.querySelector("input[name=apr]").addEventListener('input', listen_for_input);
document.querySelector("input[name=term]").addEventListener('input', listen_for_input);


function amortizedLoan() {
    if (term > 0) {
        var numberOfPayments = paymentsPerYear(term);
    }
    if (apr > 0) {
        var periodicRate = periodicInterestRate(apr);
        var calculatedDiscountFactor = discountFactor(periodicRate, numberOfPayments);
    }
    if (principle > 0 && (calculatedDiscountFactor !== undefined)){
        var interestPayment = interestOnly(principle, apr);
        var calculatedPayments = payments(principle, calculatedDiscountFactor);
        var percentOfPayment = convertToTwoDecimalSpots((interestPayment * 100)/calculatedPayments);
    }
    if ((!notBlank) && (calculatedPayments !== undefined && calculatedPayments !== 'NaN')){
        var paymentSchedule = amortizedSchedule(principle, apr, calculatedPayments);
        document.querySelector("#payments").innerHTML = calculatedPayments;
        document.querySelector("#length").innerHTML = term;
        document.querySelector("#interestPayment").innerHTML = interestPayment;
        document.querySelector("#interestPercent").innerHTML = percentOfPayment;
        document.querySelector("#results").style.display = "block";
        return paymentSchedule;
    } else if ((notBlank === true) || (calculatedPayments === (undefined || 'NaN'))){
        document.querySelector("#results").style.display= "none";
        document.querySelector("#chart").style.display = "none";
        return null
    }
}

var principleInput = document.querySelector("input[name=principle]");

principleInput.onfocus = formatPrincipleAsNumber;
principleInput.onblur = formatPrincipleAsCurrency;

function formatPrincipleAsNumber(){
        principleInput.type = 'number';
        if(principle){
            principleInput.value = Number(
                parseFloat(principle).toFixed(2));
        }
        else{
            principleInput.value = '';
        }
}

function formatPrincipleAsCurrency() {
    let options = { style: 'currency', currency: 'USD' };
    let numberFormat = new Intl.NumberFormat('en-US', options);
    if(principle){ 
        principleInput.type = 'text'
        principleInput.value = numberFormat.format(Number(
            parseFloat(principle).toFixed(2)))
        } 
    else {
        principleInput.value = '';
        } 
}

amortizedSchedule = function (principle, apr, amortizedPayment){
    let principleBalance = [], 
    monthlyPrinciplePaid = [], monthlyInterestPaid = [],
    yearEndPrincipleBalance = [], yearEndInterestBalance = []; 
    let totalInterestPaid = 0, counter = 1, year = 0;
    let startingPrinciple = principle;
    let fixedPayment = amortizedPayment;
    let currentMonthsInterest = interestOnly(startingPrinciple, apr);
    let currentMonthsPrinciple = Number((fixedPayment - currentMonthsInterest).toFixed(2));
    while (Math.round(startingPrinciple - currentMonthsPrinciple) >= 0){
        currentMonthsInterest = interestOnly(startingPrinciple, apr);
        currentMonthsPrinciple = Number((fixedPayment - currentMonthsInterest).toFixed(2));
        monthlyInterestPaid.push(currentMonthsInterest);
        monthlyPrinciplePaid.push(currentMonthsPrinciple);
        startingPrinciple -= currentMonthsPrinciple;
        totalInterestPaid = Number((totalInterestPaid + currentMonthsInterest).toFixed(2));
        principleBalance.push(Number(startingPrinciple.toFixed(2)));
        if(((counter !== 0) && (counter % 12 === 0)) || (Math.round(startingPrinciple - currentMonthsPrinciple) <= currentMonthsPrinciple)){
            year++
            yearEndPrincipleBalance.push(principleBalance[principleBalance.length-1])
            yearEndInterestBalance.push(totalInterestPaid)

        }
        counter++
    }
    return { monthlyInterest: monthlyInterestPaid,
            monthlyPrinciplePaid: monthlyPrinciplePaid,  
            totalInterestPaid: totalInterestPaid,
            monthlyPrincipleBalance: principleBalance,
            yearEndBalance: {'year' : year, yearEndPrincipleBalance},
            yearEndInterest:{'year' : year, yearEndInterestBalance}
    }
}

function chartData(paymentSchedule){
    // Sequence generator function (commonly referred to as "range", e.g. Clojure, PHP etc)
    const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
    var ctx = document.getElementById('chart').getContext('2d');
    let numberOfYears =  paymentSchedule.yearEndBalance.year - 1
    let years = range(1, numberOfYears, 1);
    years = years.map( x => `Year ${x}`)
    let options = { style: 'currency', currency: 'USD' };
    let numberFormat = new Intl.NumberFormat('en-US', options);
    var myChart = new Chart(ctx, {
    type: numberOfYears >= 9 ? 'bar' : 'horizontalBar',
    data: {
        labels: years,
        datasets: [{
            label: ['Balance'],
            data: paymentSchedule.yearEndBalance.yearEndPrincipleBalance.map(x => x),
            hoverBackgroundColor: 'rgba(255, 99, 132, 0.7)',	
            backgroundColor:
                'rgba(255, 99, 132, 0.2)',
            borderColor: 
                'rgba(255, 99, 132, 1)',
            borderWidth: 1
        },
        {
            label: ['Interest'],
            data:
                paymentSchedule.yearEndInterest.yearEndInterestBalance.map(x => x),
            hoverBackgroundColor: 'rgba(54, 162, 235, 0.7)',	
            backgroundColor:
                'rgba(54, 162, 235, 0.2)',
            borderColor:
                'rgba(54, 162, 235, 1)',
            borderWidth: 1
        },

    ],

    },
    options: {
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    min: 0,
                },
                stacked: true
            }]
            // yAxes: [{
            //     ticks: {
            //         beginAtZero: true,
            //         min: 0,
            //     }
            // }]
        }
    }
    });
    return myChart
};