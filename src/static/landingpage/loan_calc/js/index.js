var principle, apr, term;
var notBlank = false;
function convertToTwoDecimalSpots(number){
    return (Math.round(number * 100)/100).toFixed(2);
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
    let rate = (parseFloat(APR)/100).toFixed(2);
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
    let YearlyAPR =  ((parseFloat(APR)/100).toFixed(2))/12
    let Payments = Math.round(loanAmount * YearlyAPR)
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
            term = e.target.value;
            break;
        case 'principle':
            principle = e.target.value;
            break;
        case 'apr':
            apr = e.target.value;
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
    amortizedLoan()
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
        var percentOfPayment = convertToTwoDecimalSpots((interestPayment * 100)/calculatedPayments)
    }
    if ((!notBlank) && (calculatedPayments !== undefined && calculatedPayments !== 'NaN')){
        document.querySelector("#payments").innerHTML = calculatedPayments;
        document.querySelector("#length").innerHTML = term;
        document.querySelector("#interestPayment").innerHTML = interestPayment;
        document.querySelector("#interestPercent").innerHTML = percentOfPayment;
        document.querySelector("#results").style.display = "block";
    } else if ((notBlank === true) || (calculatedPayments === (undefined || 'NaN'))){
        document.querySelector("#results").style.display= "none";

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
            principleInput.value = 0;
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
        principleInput.value = numberFormat.format(0)
        } 
}