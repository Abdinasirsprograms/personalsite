let displayChart;
// example: loan of 10k at 3% for 7 years 
// n = 84 (12 monthly payments/year * 7 years)  🏁 part of getPaymentPeriod
// r = 0.0025 (0.03/by 12 payments per year) 🏁 part of getPaymentPeriod
// D = 75.6813 {[(1+0.0025)^84] - 1} / 0.0025(1+0.0025)^84
// P = $132.13 (10,000/75.6813)
// calculating the interest only payment on the above example:
// Payment = Amount * (APR/12)
// P = $25 (10,000 * (0.03/12))


const setParams = class {
    constructor(){
        this._principle = 0
        this._apr = 0
        this._termLength = 0
    };

    /**
     * @param {float} principle
     */
    set setPrinciple(principle){
        this._principle = Number(parseFloat(principle).toFixed(2))
    };

    /**
     * @param {float} apr
     */
    set setApr(apr){
        this._apr = Number(parseFloat(apr).toFixed(2))
    };

    /**
     * @param {int} termLength
     */
    set setTermLength(termLength){
        termLength = parseInt(termLength)
        if (termLength > 0){
            this._termLength = termLength
        }else {
            this._termLength = 0
        };
    };
    
    get getPrinciple() {
        return this._principle
    };

    get getApr() {
        return this._apr
    };

    get getTermLength() {
        return this._termLength
    };

    get getParams() {
        return {'principle': this._principle, 'apr': this._apr, 'termLength': this._termLength}
    };

    convertToTwoDecimal(number){
        return Number((Math.round(number * 100)/100).toFixed(2));
    };
};

const getPaymentPeriod = class extends setParams{
    constructor(){
        super()
        this._termPeriod = ''
    }

    /**
     * @param {string} termPeriod
     */
    set setTermPeriod(termPeriod) {
        let type = typeof(termPeriod);
        if (type === 'string'){
            this._termPeriod = termPeriod;
        }
        else{
            throw new TypeError(`Invalid type passed: ${type}, Expcted Type: string`);
        }; 
    };

    get getTermPeriod(){
        return this._termPeriod
    }
    get getPaymentTerm(){
            return this.getTermPeriod === 'month' ? this.getTermLength : this.getTermLength * 12
    };

    getMonthlyInterestRate(APR) {
        APR = Number(parseFloat(APR).toFixed(2))
        if(APR > 1){
            APR = Number((APR/100).toFixed(2));
        }
        return APR/12;
    };
};

const CalculatePayment = class extends getPaymentPeriod {
    constructor(){
        super()
        this._payment = 0
    };

    /**
     * @param {float} payment
     */
    set setPayment(payment){
        this.payment = Number(parseFloat(payment).toFixed(2))
    };

    get getPayment(){
        this.payment()
        return this._payment
    };

    get getMonthlyRate(){
        return this.PeriodicRate()
    } 

    getInterestPayment(principle){
        return this.interestOnlyPayment(principle)
    }
    
    PeriodicRate(){
        let returnedRate = this.getMonthlyInterestRate(this.getApr)
        if (typeof(returnedRate) === 'number'){
            this._periodicRate = returnedRate
            return this._periodicRate
        }
        else {
            throw Error('getMonthlyInterestRate returned invalid value')
        }
    };

    getDiscountFactor() {
        let paymentPeriod = this.getPaymentTerm;
        let rate = this.getMonthlyRate
        let rateAddOne = rate + 1;
        let rateMulitpliedByPaymentPeriods = rateAddOne ** paymentPeriod;
        let DiscountFactor = (rateMulitpliedByPaymentPeriods - 1)/(rate * rateMulitpliedByPaymentPeriods);
        return DiscountFactor;
    };

    payment(){
        let payment = this.getPrinciple/this.getDiscountFactor()
        this._payment = this.convertToTwoDecimal(payment)
    };

    interestOnlyPayment(principle) {
        let rate = this.getMonthlyRate
        this._interestPayments = (principle * rate)
        return this._interestPayments
    }
};

const amortizeSchedule = class extends CalculatePayment{
    constructor() {
        super()
        this.monthlyInterestPayments = [];
        this.monthlyPrinciplePayments = [];
        this.monthlyTotalPrinciple = [];
        this.totalAnnualPayments = [];
        this.totalAnnualInterests = [];
        this.totalAnnualPrinciples = [];
        this.totalInterestPaid = 0;
        this.totalPrinciplePaid = 0;
        this.totalPaid = 0;
        this.Calculated = false;
    }
    resetParams(){
        this.monthlyInterestPayments = [];
        this.monthlyPrinciplePayments = [];
        this.monthlyTotalPrinciple = [];
        this.totalAnnualPayments = [];
        this.totalAnnualInterests = [];
        this.totalAnnualPrinciples = [];
        this.totalInterestPaid = 0;
        this.totalPrinciplePaid = 0;
        this.totalPaid = 0;
    }
    get getTotalAnnualInterests(){
        return this.totalAnnualInterests       
    }

    get getTotalAnnualPrinciples(){
        return this.totalAnnualPrinciples       
    }

    get getTotalAnnualPayments(){
        return this.totalAnnualPayments       
    }

    get schedule(){
        if(this.getParams.apr > 0 && this.getParams.principle > 0 && this.getParams.termLength > 0){
            this.startSchedule()
            return
        }
        this.Calculated = false
        this.resetParams()
        return
    }
    
    displayResults(){
        document.querySelector("#payments").innerHTML = Calc.getPayment;
        document.querySelector("#length").innerHTML = Calc.getPaymentTerm/12;
        document.querySelector("#interestPayment").innerHTML = Calc.getInterestPayment(Calc.getPrinciple);
        document.querySelector("#interestPercent").innerHTML = Calc.convertToTwoDecimal((Calc.getInterestPayment(Calc.getPrinciple)/Calc.getPayment)*100);
        document.querySelector("#results").style.display = "block";
    }
    
    hideResults(){
        document.querySelector("#results").style.display = "none";
    }
    startSchedule() {
        let principle = this.getPrinciple;
        let monthlyInterest = this.getInterestPayment(principle);
        let payment = this.getPayment;
        let monthlyPay = payment - monthlyInterest;
        let monthlyCounter = 1; 
        let rollingInterestPayments = 0
        while(principle >= 1){
            this.monthlyPrinciplePayments.push(this.convertToTwoDecimal(monthlyPay))
            rollingInterestPayments += monthlyInterest
            this.monthlyInterestPayments.push(this.convertToTwoDecimal(monthlyInterest))
            principle -= monthlyPay 
            this.monthlyTotalPrinciple.push(this.convertToTwoDecimal(principle))
            this.totalInterestPaid += monthlyInterest 
            this.totalPrinciplePaid += monthlyPay 
            this.totalPaid = this.totalInterestPaid + this.totalPrinciplePaid
            monthlyInterest = this.getInterestPayment(principle)
            monthlyPay = payment - monthlyInterest;
            if(monthlyCounter !== 0 && monthlyCounter % 12 === 0){
                this.totalAnnualInterests.push(this.convertToTwoDecimal(Math.round(this.totalInterestPaid)))
                this.totalInterestPaid = 0;
                this.totalAnnualPrinciples.push(this.convertToTwoDecimal(Math.round(this.totalPrinciplePaid)))
                this.totalPrinciplePaid = 0;
                this.totalAnnualPayments.push(this.convertToTwoDecimal(Math.round(principle)))
            }
            monthlyCounter++
        }
        this.totalPaid = this.convertToTwoDecimal(this.totalPaid)
        this.totalInterestPaid = this.convertToTwoDecimal(this.totalInterestPaid)
        this.totalPrinciplePaid = this.convertToTwoDecimal(this.totalPrinciplePaid)
        this.Calculated = true
    }
};

const Calc = new amortizeSchedule
Calc.setTermPeriod = 'years'

function listen_for_input(e) {
    switch(e.target.name){
        case 'term':
            Calc.setTermLength = e.target.value;
            break;
        case 'principle':
            Calc.setPrinciple = e.target.value;
            break;
        case 'apr':
            Calc.setApr = e.target.value;
            break;
        default:
            console.log('None')
            break;
    }
    Calc.resetParams()
    Calc.schedule
    if(displayChart && Calc.Calculated){
        displayChart.destroy()
        displayChart = chartData();
        Calc.displayResults()
        document.querySelector("#chart").style.display = "block";
    }
    else if (Calc.Calculated) {
        displayChart = chartData();
        Calc.displayResults()
        document.querySelector("#chart").style.display = "block";
    }
    else if(displayChart && Calc.getTermLength <= 1) {
        displayChart.destroy()
        Calc.resetParams()
        Calc.hideResults()
        document.querySelector("#results").style.display = "none";
        document.querySelector("#chart").style.display = "none";
    }
    return 
}

document.querySelector("input[name=principle]").addEventListener('input', listen_for_input);
document.querySelector("input[name=apr]").addEventListener('input', listen_for_input);
document.querySelector("input[name=term]").addEventListener('input', listen_for_input);


const formatPrincipleAsNumber = function () {
        principleInput.type = 'number';
        if(Calc.getPrinciple){
            principleInput.value = Number(
                parseFloat(Calc.getPrinciple).toFixed(2));
        }
        else{
            principleInput.value = '';
        }
}

const formatPrincipleAsCurrency = function() {
    let options = { style: 'currency', currency: 'USD' };
    let numberFormat = new Intl.NumberFormat('en-US', options);
    if(Calc.getPrinciple){ 
        principleInput.type = 'text'
        principleInput.value = numberFormat.format(Number(
            parseFloat(Calc.getPrinciple).toFixed(2)))
        } 
    else {
        principleInput.value = '';
        } 
}

const principleInput = document.querySelector("input[name=principle]");

principleInput.onfocus = formatPrincipleAsNumber;
principleInput.onblur = formatPrincipleAsCurrency;


const chartData = function(){
    // Sequence generator function (commonly referred to as "range", e.g. Clojure, PHP etc)
    const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
    let ctx = document.getElementById('chart').getContext('2d');
    let numberOfYears =  Calc.getTotalAnnualPrinciples.length
    let years = range(1, numberOfYears, 1);
    years = years.map( x => `Year ${x}`)
    let options = { style: 'currency', currency: 'USD' };
    let numberFormat = new Intl.NumberFormat('en-US', options);
    let myChart = new Chart(ctx, {
        type: numberOfYears >= 9 ? 'bar' : 'horizontalBar',
        data: {
            labels: years,
            datasets: [
            {
                label: 'Principle',
                data: Calc.getTotalAnnualPrinciples.map(x => x),
                hoverBackgroundColor: 'rgba(255, 99, 132, 0.7)',	
                backgroundColor:
                    'rgba(255, 99, 132, 0.2)',
                borderColor: 
                    'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Interest',
                data:
                    Calc.getTotalAnnualInterests.map(x => x),
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
            }
        }
    });
    return myChart
};