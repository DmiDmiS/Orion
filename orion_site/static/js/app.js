(function () {
  // ---- Печать одного договора или всего списка ----
  window.printRow = function (btn) {
    var row = btn.closest('tr');
    document.querySelectorAll('tr.print-target').forEach(function (r) { r.classList.remove('print-target'); });
    row.classList.add('print-target');
    document.body.classList.add('print-single');
    window.print();
  };
  window.addEventListener('afterprint', function () {
    document.body.classList.remove('print-single');
    document.querySelectorAll('tr.print-target').forEach(function (r) { r.classList.remove('print-target'); });
  });

  // ---- Диаграммы на canvas ----
  function niceMax(m) {
    if (m <= 0) return 1;
    var exp = Math.pow(10, Math.floor(Math.log10(m))), f = m / exp;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * exp;
  }

  function drawBars(canvas, labels, values, opt) {
    var dpr = window.devicePixelRatio || 1, w = canvas.clientWidth, h = canvas.clientHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    var c = canvas.getContext('2d');
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.fillStyle = '#fff'; c.fillRect(0, 0, w, h);
    c.font = '12px Arial, sans-serif'; c.textBaseline = 'middle';

    // легенда
    c.fillStyle = opt.color; c.fillRect(w / 2 - 70, 12, 38, 12);
    c.fillStyle = '#333'; c.textAlign = 'left'; c.fillText(opt.legend, w / 2 - 28, 18);

    if (!values.length) {
      c.textAlign = 'center'; c.fillStyle = '#6c757d';
      c.fillText('Нет данных для отображения', w / 2, h / 2);
      return;
    }
    var L = 78, R = 16, T = 40, B = 34, pw = w - L - R, ph = h - T - B;
    var max = niceMax(Math.max.apply(null, values)), steps = 5;
    c.textAlign = 'right'; c.strokeStyle = '#e3e6ea'; c.fillStyle = '#555';
    for (var i = 0; i <= steps; i++) {
      var y = T + ph - (ph * i / steps), v = max * i / steps;
      c.beginPath(); c.moveTo(L, y); c.lineTo(w - R, y); c.stroke();
      c.fillText(v.toLocaleString('ru-RU'), L - 8, y);
    }
    var slot = pw / values.length, bw = Math.min(slot * 0.6, 120);
    values.forEach(function (val, i) {
      var bh = ph * val / max, x = L + slot * i + (slot - bw) / 2;
      c.fillStyle = opt.color; c.fillRect(x, T + ph - bh, bw, bh);
      c.fillStyle = '#555'; c.textAlign = 'center';
      c.fillText(labels[i], x + bw / 2, T + ph + 16);
    });
  }

  var dataEl = document.getElementById('chart-data');
  if (dataEl) {
    var data = JSON.parse(dataEl.textContent);
    var render = function () {
      drawBars(document.getElementById('chart-contracts'), data.contracts.labels, data.contracts.values,
        { color: '#ffb3c6', legend: 'Статистика договоров' });
      drawBars(document.getElementById('chart-sales'), data.sales.labels, data.sales.values,
        { color: '#ffee00', legend: 'Движение продаж, руб.' });
    };
    render();
    window.addEventListener('resize', render);
    document.querySelectorAll('[data-save]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var a = document.createElement('a');
        a.download = btn.getAttribute('data-file');
        a.href = document.getElementById(btn.getAttribute('data-save')).toDataURL('image/png');
        a.click();
      });
    });
  }
})();
