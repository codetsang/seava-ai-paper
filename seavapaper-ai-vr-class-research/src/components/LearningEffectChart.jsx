import ReactECharts from 'echarts-for-react'

const dimensions = ['口语流利度', '表达自信心', '情景代入感', '课堂参与度', '综合口语技能']
const before = [62.4, 55.1, 48.6, 57.8, 60.2]
const after = [81.2, 84.3, 87.9, 85.6, 78.7]

const option = {
  color: ['#4472C4', '#C00000'],
  textStyle: { fontFamily: 'SimSun, Songti SC, serif', fontSize: 11 },
  legend: {
    data: ['升级前', '升级后'],
    top: 0,
    itemWidth: 18,
    itemHeight: 10,
    textStyle: { fontSize: 11 },
  },
  grid: { left: 88, right: 20, top: 36, bottom: 32 },
  xAxis: {
    type: 'category',
    data: dimensions,
    axisLabel: { fontSize: 10, interval: 0 },
    axisTick: { alignWithLabel: true },
  },
  yAxis: {
    type: 'value',
    name: '得分',
    min: 40,
    max: 100,
    nameTextStyle: { fontSize: 10, padding: [0, 0, 0, -28] },
    splitLine: { lineStyle: { type: 'dashed', color: '#E0E0E0' } },
  },
  series: [
    {
      name: '升级前',
      type: 'bar',
      barWidth: 22,
      data: before,
      label: { show: true, position: 'top', fontSize: 9, formatter: '{c}' },
    },
    {
      name: '升级后',
      type: 'bar',
      barWidth: 22,
      data: after,
      label: { show: true, position: 'top', fontSize: 9, formatter: '{c}' },
    },
  ],
}

export default function LearningEffectChart() {
  return (
    <ReactECharts
      option={option}
      style={{ height: 280, width: '100%' }}
      opts={{ renderer: 'svg' }}
    />
  )
}
