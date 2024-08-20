// graficos.js
document.addEventListener('DOMContentLoaded', function() {
    const ctxDiario = document.getElementById('grafico-diario').getContext('2d');
    const ctxMensal = document.getElementById('grafico-mensal').getContext('2d');

    // Função para criar gráficos de pizza
    function criarGraficoPizza(ctx, valorAtual, valorLimite) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Utilizado', 'Restante'],
                datasets: [{
                    label: 'Porcentagem',
                    data: [valorAtual, valorLimite - valorAtual],
                    backgroundColor: [
                        '#ff8a80', // pastel coral
                        '#e0e7f0'  // pastel light blue
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const data = tooltipItem.dataset.data;
                                const total = data[0] + data[1];
                                const value = data[tooltipItem.dataIndex];
                                const percentage = ((value / total) * 100).toFixed(2);
                                const label = tooltipItem.label;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Obter valores dos gráficos e criar os gráficos
    const valorLimiteDiario = parseFloat(document.querySelector('#grafico-diario + .valor-limite').textContent);
    const valorUtilizadoDiario = valorLimiteDiario * 0.5; // Exemplo: 50% utilizado
    criarGraficoPizza(ctxDiario, valorUtilizadoDiario, valorLimiteDiario);

    const valorLimiteMensal = parseFloat(document.querySelector('#grafico-mensal + .valor-limite').textContent);
    const valorUtilizadoMensal = valorLimiteMensal * 0.3; // Exemplo: 30% utilizado
    criarGraficoPizza(ctxMensal, valorUtilizadoMensal, valorLimiteMensal);
});
