import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as echarts from 'echarts'

const app = createApp({
    data() {
        return {
            alerts: [],
            logData: {
                total: 0,
                items: []
            },
            stats: {}
        }
    },
    mounted() {
        this.loadData()
        this.setupCharts()
    },
    methods: {
        async loadData() {
            try {
                // 获取告警数据
                const alertsRes = await axios.get('/api/alerts')
                this.alerts = alertsRes.data

                // 获取日志统计
                const statsRes = await axios.get('/api/logs/stats')
                this.stats = statsRes.data

                // 获取最近日志
                const logsRes = await axios.get('/api/logs/recent')
                this.logData = logsRes.data

            } catch (error) {
                console.error('加载数据失败:', error)
            }
        },
        setupCharts() {
            // 状态码分布图
            const statusChart = echarts.init(document.getElementById('status-chart'))
            statusChart.setOption({
                title: { text: '状态码分布' },
                tooltip: {},
                series: [{
                    name: '状态码',
                    type: 'pie',
                    data: Object.entries(this.stats.status_codes || {}).map(([name, value]) => ({ name, value }))
                }]
            })
        }
    }
})

app.use(ElementPlus)
app.mount('#app')