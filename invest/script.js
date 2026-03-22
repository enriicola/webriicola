const ctx = document.getElementById('mainChart').getContext('2d');
let chart;

function calculate() {
    const invested = parseFloat(document.getElementById('initial').value) || 0;
    const idleCash = parseFloat(document.getElementById('idleCash').value) || 0;
    const years = parseInt(document.getElementById('years').value) || 0;
    const rate = (parseFloat(document.getElementById('return').value) || 0) / 100;
    const finecoSingleFee = parseFloat(document.getElementById('finecoFee').value) || 0;
    const trRate = (parseFloat(document.getElementById('trInterest').value) || 0) / 100;

    // Parametri dinamici per la simulazione
    const tradesPerYear = parseInt(document.getElementById('tradesPerYear').value) || 0;
    const timingEfficiency = (parseInt(document.getElementById('timingEfficiency').value) || 70) / 100;
    document.getElementById('effVal').innerText = Math.round(timingEfficiency * 100);

    const labels = Array.from({length: years + 1}, (_, i) => i);
    const strategyTR = []; 
    const strategyFineco = []; 

    // Strategia Passiva (Trade Republic): Commissione minima iniziale
    let trInvested = invested > 0 ? invested - 1 : 0;
    let trCash = idleCash;
    
    // Strategia Market Timing (Fineco): Commissioni ricorrenti e rendimento variabile
    let ftInvested = invested;
    let ftCash = idleCash;
    
    const STAMP_DUTY = 34.20; // Imposta di bollo su giacenza > 5k
    const annualFinecoFees = finecoSingleFee * tradesPerYear;

    for (let i = 0; i <= years; i++) {
        strategyTR.push(Math.round(trInvested + trCash));
        strategyFineco.push(Math.round(ftInvested + ftCash));
        
        // Crescita Trade Republic
        trInvested = (trInvested * (1 + rate));
        trCash = trCash * (1 + trRate);
        if (trCash >= 5000) trCash -= STAMP_DUTY;
        
        // Crescita Fineco (Rendimento ridotto dall'efficienza del timing)
        if (ftCash >= 5000) ftCash -= STAMP_DUTY;
        ftInvested = (ftInvested * (1 + (rate * timingEfficiency))) - annualFinecoFees;
        
        if (ftInvested < 0) ftInvested = 0; 
    }

    const finalTR = strategyTR[strategyTR.length - 1];
    const finalFineco = strategyFineco[strategyFineco.length - 1];
    const totalGap = finalTR - finalFineco;
    
    const netCashTR = trCash - idleCash;

    updateUI(finalTR, totalGap, Math.round(netCashTR), years, labels, strategyTR, strategyFineco);
}

function updateUI(finalTR, totalGap, netCashTR, years, labels, tr, fi) {
    document.getElementById('finalVal').innerText = finalTR.toLocaleString('it-IT', {maximumFractionDigits: 0}) + '€';
    document.getElementById('feeDrag').innerText = totalGap.toLocaleString('it-IT', {maximumFractionDigits: 0}) + '€';
    document.getElementById('cashGain').innerText = netCashTR.toLocaleString('it-IT', {maximumFractionDigits: 0}) + '€';
    document.querySelectorAll('.yearLabel').forEach(el => el.innerText = years);

    if (chart) chart.destroy();
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Trade Republic (Passivo)',
                    data: tr,
                    borderColor: '#2563eb',
                    fill: false,
                    tension: 0.3
                },
                {
                    label: 'Fineco (Market Timing)',
                    data: fi,
                    borderColor: '#dc2626',
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { 
                    beginAtZero: false, 
                    title: { display: true, text: 'Patrimonio Totale (€)' } 
                },
                x: { title: { display: true, text: 'Anni' } }
            }
        }
    });
}

document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', calculate);
});

calculate();
