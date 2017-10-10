<template>
  <div class="row">
    <div class="col-md-10">
      <b-card>
        <!--Somehow title is undefined <h6>{{title}}</h6>-->
        <h6>Chromosome 6</h6>
        <div id="bars"></div>
      </b-card>
    </div>
    <div class="col-md-2">
      <selected-band-information :band="band" :start="start" :stop="stop"></selected-band-information>
    </div>
  </div>
</template>

<script>
  import * as d3 from 'd3'
  import SelectedBandInformation from './SelectedBandInformation'

  export default {
    name: 'd3-chromo-chart',
    components: {SelectedBandInformation},
    computed: {
      clickContent: {
        get: function () {
          return this.selected
        },
        set: function (content) {
          this.band = content.split(',')[0]
          this.start = content.split(',')[1]
          this.stop = content.split(',')[2]
          if (this.selected !== content) {
            this.selected = 'Selected:<br/>' + content
          }
        }
      }
    },
    data: function () {
      return {
        selected: 'Selected: ',
        band: '',
        start: '',
        stop: '',
        chr: [[0, 2300000, 'p25.3'], [2300000, 4200000, 'p25.2'], [4200000, 7100000, 'p25.1'],
          [7100000, 10600000, 'p24.3'], [10600000, 11600000, 'p24.2'], [11600000, 13400000, 'p24.1'],
          [13400000, 15200000, 'p23'], [15200000, 25200000, 'p22.3'], [25200000, 27000000, 'p22.2'],
          [27000000, 30400000, 'p22.1'], [30400000, 32100000, 'p21.33'], [32100000, 33500000, 'p21.32'],
          [33500000, 36600000, 'p21.31'], [36600000, 40500000, 'p21.2'], [40500000, 46200000, 'p21.1'],
          [46200000, 51800000, 'p12.3'], [51800000, 52900000, 'p12.2'], [52900000, 57000000, 'p12.1'],
          [57000000, 58700000, 'p11.2'], [58700000, 61000000, 'p11.1'], [61000000, 63300000, 'q11.1'],
          [63300000, 63400000, 'q11.2'], [63400000, 70000000, 'q12'], [70000000, 75900000, 'q13'],
          [75900000, 83900000, 'q14.1'], [83900000, 84900000, 'q14.2'], [84900000, 88000000, 'q14.3'],
          [88000000, 93100000, 'q15'], [93100000, 99500000, 'q16.1'], [99500000, 100600000, 'q16.2'],
          [100600000, 105500000, 'q16.3'], [105500000, 114600000, 'q21'], [114600000, 118300000, 'q22.1'],
          [118300000, 118500000, 'q22.2'], [118500000, 126100000, 'q22.31'], [126100000, 127100000, 'q22.32'],
          [127100000, 130300000, 'q22.33'], [130300000, 131200000, 'q23.1'], [131200000, 135200000, 'q23.3'],
          [135200000, 139000000, 'q23.3'], [139000000, 142800000, 'q24.1'], [142800000, 145600000, 'q24.2'],
          [145600000, 149000000, 'q24.3'], [149000000, 152500000, 'q25.1'], [152500000, 155500000, 'q25.2'],
          [155500000, 161000000, 'q25.3'], [161000000, 164500000, 'q26'], [164500000, 171115067, 'q27']
        ],
        chr_centromere: 61000000
      }
    },
    props: ['mutations', 'figureWidth', 'chr_size', 'height', 'patientIds', 'title'],
    mounted () {
      this.renderChart()
    },
    methods: {
      drawChromText (chr, fontsize, band, id, y, x) {
        chr.append('text')
          .attr('font-size', fontsize)
          .attr('fill', 'black')
          .attr('id', id + '_' + band + '_desc')
          .attr('x', x)
          .attr('y', y)
          .text(function () {
            return band
          })
      },
      drawChromRect (chr, size, band, className, id, x, ry, rx, start, stop) {
        let self = this
        chr.append('rect')
          .attr('width', size)
          .attr('height', 19)
          .attr('id', id + '_' + band)
          .attr('class', className)
          .attr('x', x)
          .attr('y', 20)
          .attr('stroke', 'black')
          .attr('rx', rx)
          .attr('ry', ry)
          .attr('start', start)
          .attr('stop', stop)
          .attr('band', band)
        d3.selectAll('rect')
          .on('click', function () {
            self.clickBand(this)
          })
      },
      drawChromBand (chr, size, evenOrOdd, id, y, x, fontsize, band, start, stop) {
        this.drawChromRect(chr, size, band, 'chromosome-band-' + evenOrOdd, id, x, 0, 0, start, stop)
        this.drawChromText(chr, fontsize, band, id, y, x)
      },
      clickBand ($this) {
        let self = this
        const band = d3.select($this)
        const bandName = band.attr('band')
        const start = band.attr('start')
        const stop = band.attr('stop')
        self.clickContent = bandName + ',' + start + ',' + stop
      },
      makeChromosome (id, transform, center) {
        let centromerePos = this.chr_size / center
        let barstop = this.figureWidth / centromerePos
        d3.select('#bars').append('div').attr('id', 'chr_container_' + id).attr('class', 'chr_container')
        let chr = d3.select('#chr_container_' + id).append('svg')
          .attr('width', this.figureWidth + 100)
          .attr('height', 70).append('g')
          .attr('transform', 'translate(0,' + transform + ')')
        const fontsize = 10
        let self = this
        self.drawChromRect(chr, barstop, 'p-arm', 'chromosome', id, 0, 10, 10, 0, center)
        self.drawChromRect(chr, self.figureWidth - barstop, 'q-arm', 'chromosome', id, barstop, 10, 10, center, self.chr_size)
        self.chr.map(function (band, i) {
          let start = self.figureWidth / (self.chr_size / band[0])
          let size = self.figureWidth / (self.chr_size / (band[1] - band[0]))
          if (i === 0) {
            self.drawChromText(chr, fontsize, band[2], id, 10, 0)
          } else if (i === self.chr.length - 1) {
            self.drawChromText(chr, fontsize, band[2], id, 10, self.figureWidth)
          } else if (band[0] === center || band[1] === center) {
          } else if (i % 2 === 0) {
            if (i % 4 === 0) {
              self.drawChromBand(chr, size, 'even', id, 7, start, fontsize, band[2], band[0], band[1])
            } else {
              self.drawChromBand(chr, size, 'even', id, 17, start, fontsize, band[2], band[0], band[1])
            }
          } else {
            if (i % 4 === 1) {
              self.drawChromBand(chr, size, 'odd', id, 55, start, fontsize, band[2], band[0], band[1])
            } else {
              self.drawChromBand(chr, size, 'odd', id, 65, start, fontsize, band[2], band[0], band[1])
            }
          }
        })
        return chr
      },
      makeBar (chart, patientId, transform) {
        const bar = chart.append('g')
          .attr('transform', 'translate(0,' + transform + ')')
        bar.append('rect')
          .attr('width', this.figureWidth)
          .attr('height', 19)
          .attr('id', 'total' + patientId)
          .attr('class', 'background-bar')
        return bar
      },
      addMutations (bar, patientMutations, patientId) {
        const self = this
        patientMutations.map(function (mutation) {
//          console.log('mutations', mutation, patientId)
          let bp = self.figureWidth / self.chr_size
          let size = mutation.stop - mutation.start
          bar.append('rect').attr('width', size * bp).attr('height', self.height).attr('x', bp * mutation.start)
            .attr('id', patientId).attr('class', mutation.type)
        })
      },
      renderChart () {
        const self = this
        console.log(self.title)
        self.makeChromosome('chromosome6', 1, self.chr_centromere)
//        self.patientIds.map(function (patientId, i) {
//          d3.select('#bars').append('div').attr('id', 'patient_container_' + patientId)
//          let patientContainer = d3.select('#patient_container_' + patientId)
//          patientContainer.append('div').attr('class', patientId).append('svg')
//            .attr('class', 'chart').attr('id', 'patient' + patientId)
//          let chart = d3.select('#patient' + patientId).attr('width', self.figureWidth).attr('height', self.height)
//          let bar = self.makeBar(chart, patientId, i + 2)
//          self.addMutations(bar, self.mutations[patientId], patientId)
//        })
      }
    }
  }
</script>

<style>
  .d3-header {
    color: black;
  }

  svg {
    /*background-color: rgba(255, 111, 152, 0.24);*/
    margin: 25px;
  }

  .line {
    fill: none;
    stroke: steelblue;
    stroke-width: 3px;
  }

  rect.chromosome {
    fill: grey;
  }

  rect.chromosome-band-even {
    fill: white;
  }

  rect.chromosome-band-odd {
    fill: black;
  }

  rect.background-bar {
    fill: #99CCFF;
  }

  rect.del {
    fill: orange
  }

  rect.dup {
    fill: steelblue
  }

  .chr_container {
    border-radius: 15px;
  }
</style>
