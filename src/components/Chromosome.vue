<template>
  <div class="row">
    <div class="col-md-10">
      <div id="bars"></div>
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
    name: 'chromosome',
    components: {SelectedBandInformation},
    watch: {
      selected: function () {
        this.renderChart()
      }
    },
    computed: {
      chr_centromere: function () {
        let prevVal = 'p'
        for (var value of this.chr) {
          if (prevVal.startsWith('p') && value[2].startsWith('q')) {
            return value[0]
          } else {
            prevVal = value[2]
          }
        }
      },
      chr_size: function () {
        return this.chr.slice(-1)[0][1]
      },
      clickContent: {
        get: function () {
          return this.selected
        },
        set: function (content) {
          this.band = content.split(',')[0]
          this.start = content.split(',')[1]
          this.stop = content.split(',')[2]
        }
      }
    },
    data: function () {
      return {
        band: '',
        start: '',
        stop: ''
      }
    },
    props: ['figureWidth', 'chr', 'selected'],
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
          .attr('height', 25)
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
        let chromosomeContainer = d3.select('#chr_container_' + id).append('svg')
          .attr('width', this.figureWidth + 100)
          .attr('height', 70).append('g')
          .attr('transform', 'translate(2,' + transform + ')')
        const fontsize = 10
        let self = this
        self.drawChromRect(chromosomeContainer, barstop, 'p-arm', 'chromosome', id, 0, 10, 10, 0, center)
        self.drawChromRect(chromosomeContainer, self.figureWidth - barstop, 'q-arm', 'chromosome', id, barstop, 10, 10, center, self.chr_size)
        self.chr.map(function (band, i) {
          let start = self.figureWidth / (self.chr_size / band[0])
          let size = self.figureWidth / (self.chr_size / (band[1] - band[0]))
          if (i === 0) {
            self.drawChromText(chromosomeContainer, fontsize, band[2], id, 10, 0)
          } else if (i === self.chr.length - 1) {
            self.drawChromText(chromosomeContainer, fontsize, band[2], id, 10, self.figureWidth)
          } else if (band[0] === center || band[1] === center) {
          } else if (i % 2 === 0) {
            if (i % 4 === 0) {
              self.drawChromBand(chromosomeContainer, size, 'even', id, 7, start, fontsize, band[2], band[0], band[1])
            } else {
              self.drawChromBand(chromosomeContainer, size, 'even', id, 17, start, fontsize, band[2], band[0], band[1])
            }
          } else {
            if (i % 4 === 1) {
              self.drawChromBand(chromosomeContainer, size, 'odd', id, 55, start, fontsize, band[2], band[0], band[1])
            } else {
              self.drawChromBand(chromosomeContainer, size, 'odd', id, 65, start, fontsize, band[2], band[0], band[1])
            }
          }
        })
        return chromosomeContainer
      },
      clear () {
        d3.selectAll('.chr_container').remove()
      },
      renderChart () {
        this.clear()
        const self = this
        self.makeChromosome(self.selected, 1, self.chr_centromere)
      }
    }
  }
</script>

<style>
  svg {
    /*background-color: rgba(255, 111, 152, 0.24);*/
    margin: 25px;
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

  .chr_container {
    border-radius: 15px;
  }
</style>
