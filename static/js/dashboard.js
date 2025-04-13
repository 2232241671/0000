// 攻击地图（基于IP地理信息）
function initAttackMap() {
    const chart = echarts.init(document.getElementById('attack-map'));
    fetch('/api/attack_map')
        .then(res => res.json())
        .then(data => {
            chart.setOption({
                tooltip: {},
                visualMap: {
                    min: 0,
                    max: 100,
                    text: ['High', 'Low'],
                    inRange: { color: ['#e74c3c', '#3498db'] }
                },
                series: [{
                    name: '攻击来源',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: data.points,
                    symbolSize: val => val[2] / 10
                }]
            });
        });
}

// 实时日志流
const logStream = new EventSource('/log_stream');
logStream.onmessage = (e) => {
    const log = JSON.parse(e.data);
    updateLogTable(log);
};