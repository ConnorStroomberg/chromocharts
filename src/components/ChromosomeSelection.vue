<template>
  <div class="form-group">
    <label for="selectChromosome">Chromosome</label>
    <select class="form-control" id="selectChromosome" v-model="selectedChromosome" @change="setChromosome">
      <option value="chr1">1</option>
      <option value="chr2">2</option>
      <option value="chr3">3</option>
      <option value="chr4">4</option>
      <option value="chr5">5</option>
      <option value="chr6">6</option>
      <option value="chr7">7</option>
      <option value="chr8">8</option>
      <option value="chr9">9</option>
      <option value="chr10">10</option>
      <option value="chr11">11</option>
      <option value="chr12">12</option>
      <option value="chr13">13</option>
      <option value="chr14">14</option>
      <option value="chr15">15</option>
      <option value="chr16">16</option>
      <option value="chr17">17</option>
      <option value="chr18">18</option>
      <option value="chr19">19</option>
      <option value="chr20">20</option>
      <option value="chr21">21</option>
      <option value="chr22">22</option>
      <option value="chrX">X</option>
      <option value="chrY">Y</option>
    </select>
  </div>
</template>

<script>
  import { SET_CHROMOSOME } from '../store/mutations'

  export default {
    name: 'chromosome-selection',
    data: function () {
      return {selectedChromosome: 'chr1'}
    },
    methods: {
      setChromosome: function () {
        this.$store.commit(SET_CHROMOSOME, this.selectedChromosome)
      }
    }
  }
</script>
