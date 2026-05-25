<script>
  let price = 100;
  let quantity = 3;
  $: total = (price * quantity);
</script>

<p>{total}</p>