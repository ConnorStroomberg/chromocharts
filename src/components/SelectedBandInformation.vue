<template>
  <div>
    <small>
      <b>Band</b>: {{band}}<br/>
      <b>Genomic position</b>: {{start}}-{{stop}}<br/>
    </small>
  </div>
</template>

<script>
  export default {
    name: 'selected-dot-information',
    props: ['start', 'stop', 'band']
  }
</script>
