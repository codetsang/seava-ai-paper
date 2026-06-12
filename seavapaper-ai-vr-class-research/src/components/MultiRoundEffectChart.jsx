import ReactECharts from 'echarts-for-react'
import { evaluationScores } from '../content/reportData'

const { sessions, engagement, expression, interest } = evaluationScores

const option = {
  color: ['#2E75B6', '#548235', '#C55A11'],
  textStyle: { fontFamily: 'SimSun, Songti SC, serif', fontSize: 11 },
  legend: {
    data: ['投入程度', '表达欲望', '参与兴趣度'],
    top: 0,
    itemWidth: 18,
    itemHeight: 10,
    textStyle: { fontSize: 11 },
  },
  grid: { left: 52, right: 24, top: 46, bottom: 32 },
  xAxis: {
    type: 'category',
    data: sessions,
    axisLabel: { fontSize: 10.5, interval: 0 },
    axisTick: { alignWithLabel: true },
    axisLine: { lineStyle: { color: '#666' } },
  },
  yAxis: {
    type: 'value',
    name: '班级均值',
    min: 55,
    max: 90,
    interval: 5,
    nameTextStyle: { fontSize: 10, color: '#444' },
    axisLabel: { fontSize: 10 },
    splitLine: { lineStyle: { type: 'dashed', color: '#E0E0E0' } },
  },
  series: [
    {
      name: '投入程度',
      type: 'bar',
      barGap: '18%',
      barMaxWidth: 20,
      data: engagement,
      label: { show: true, position: 'top', fontSize: 9 },
    },
    {
      name: '表达欲望',
      type: 'bar',
      barMaxWidth: 20,
      data: expression,
      label: { show: true, position: 'top', fontSize: 9 },
    },
    {
      name: '参与兴趣度',
      type: 'bar',
      barMaxWidth: 20,
      data: interest,
      label: { show: true, position: 'top', fontSize: 9 },
    },
  ],
}

export default function MultiRoundEffectChart() {
  return (
    <ReactECharts
      option={option}
      style={{ height: 290, width: '100%' }}
      opts={{ renderer: 'svg' }}
    />
  )
}
