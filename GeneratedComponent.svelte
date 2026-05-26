<script>
  let price = 100;
  let quantity = 3;
  $: total = (price * quantity);
  $: discounted = (total * 0.9);
  $: expensive = (discounted > 250);
</script>

<p>{total}</p>
<p>{discounted}</p>
<p>{expensive}</p>