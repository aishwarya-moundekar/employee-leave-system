const API = 'https://employee-leave-system-x9i9.onrender.com';

let employeesData = [];
let leavesData = [];
let statusChart = null;

function showMsg(el, text, ok=true) {
  el.style.display = 'block';
  el.textContent = text;
  el.className = 'msg ' + (ok ? 'ok' : 'err');
  setTimeout(()=>{ el.style.display='none'; }, 4200);
}

async function fetchJSON(url, opts) {
  const r = await fetch(url, opts);
  const ct = r.headers.get('content-type') || '';
  if (!r.ok) {
    let text = await r.text();
    try { const j = JSON.parse(text); text = j.error || JSON.stringify(j); } catch(e){}
    throw new Error(`${r.status} ${r.statusText}: ${text}`);
  }
  if (ct.includes('application/json')) return r.json();
  return r.text();
}

function statusBadge(status) {
  const lower = (status || '').toLowerCase();
  if (lower === 'approved') return '<span class="badge approved">Approved</span>';
  if (lower === 'rejected') return '<span class="badge rejected">Rejected</span>';
  return '<span class="badge pending">Pending</span>';
}

function updateDashboard() {
  const totalEmp = employeesData.length;
  const pending = leavesData.filter(r => r.status === 'Pending').length;
  const approved = leavesData.filter(r => r.status === 'Approved').length;
  const rejected = leavesData.filter(r => r.status === 'Rejected').length;

  document.querySelector('#cardEmp .value').textContent = totalEmp;
  document.querySelector('#cardPend .value').textContent = pending;
  document.querySelector('#cardApp .value').textContent = approved;
  document.querySelector('#cardRej .value').textContent = rejected;
}

function renderEmployees(list) {
  const area = document.getElementById('employeesArea');
  if (!list.length) {
    area.innerHTML = '<em>No employees</em>';
    return;
  }
  let html = '<div style="overflow-x:auto;"><table><thead><tr><th>ID</th><th>Name</th><th>Balance</th></tr></thead><tbody>';
  for (const e of list) {
    html += `<tr><td>${e.employee_id}</td><td>${e.name}</td><td>${e.total_leave_balance}</td></tr>`;
  }
  html += '</tbody></table></div>';
  area.innerHTML = html;
}

function renderLeaves(list) {
  const area = document.getElementById('leavesArea');
  if (!list.length) {
    area.innerHTML = '<em>No leaves yet</em>';
    return;
  }
  let html = '<div style="overflow-x:auto;"><table><thead><tr><th>ID</th><th>Emp</th><th>Type</th><th>Start</th><th>End</th><th>Days</th><th>Status</th><th>Action</th></tr></thead><tbody>';
  for (const r of list) {
    html += `<tr>
      <td>${r.request_id}</td>
      <td>${r.employee_id}</td>
      <td>${r.leave_type}</td>
      <td>${r.start_date}</td>
      <td>${r.end_date}</td>
      <td>${r.days}</td>
      <td>${statusBadge(r.status)}</td>
      <td>${
        r.status === 'Pending'
          ? `
            <button class="chip btnApprove" data-id="${r.request_id}">Approve</button>
            <button class="chip btnReject" data-id="${r.request_id}">Reject</button>
          `
          : ''
      }</td>
    </tr>`;
  }
  html += '</tbody></table></div>';
  area.innerHTML = html;

  // Approve handler
  document.querySelectorAll('.btnApprove').forEach(btn=>{
    btn.addEventListener('click', async () => {
      const id = btn.getAttribute('data-id');
      try {
        await fetchJSON(API + `/leave/${id}`, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({status:'Approved'})
        });
        showMsg(document.getElementById('applyMsg'), 'Leave approved', true);
        loadLeaves();
        loadEmployees();
      } catch(e) {
        showMsg(document.getElementById('applyMsg'), e.message, false);
      }
    });
  });

  // Reject handler
  document.querySelectorAll('.btnReject').forEach(btn=>{
    btn.addEventListener('click', async () => {
      const id = btn.getAttribute('data-id');
      try {
        await fetchJSON(API + `/leave/${id}`, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({status:'Rejected'})
        });
        showMsg(document.getElementById('applyMsg'), 'Leave rejected', true);
        loadLeaves();
        loadEmployees();
      } catch(e) {
        showMsg(document.getElementById('applyMsg'), e.message, false);
      }
    });
  });
}

function renderStatusChart(list) {
  const ctx = document.getElementById('statusChart').getContext('2d');
  const pending = list.filter(r=>r.status === 'Pending').length;
  const approved = list.filter(r=>r.status === 'Approved').length;
  const rejected = list.filter(r=>r.status === 'Rejected').length;

  const data = [pending, approved, rejected];

  if (statusChart) {
    statusChart.destroy();
  }

  statusChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Pending','Approved','Rejected'],
      datasets: [{
        label: 'Leaves',
        data: data,
        backgroundColor: ['#eab308','#22c55e','#ef4444'],
        borderColor: '#e5e7eb',
        borderWidth: 1
      }]
    },
    options: {
      plugins: { legend: { display:false }},
      scales: {
        x: {
          grid: { color:'rgba(31,41,55,0.8)' },
          ticks:{ color:'#9ca3af' }
        },
        y: {
          beginAtZero:true,
          grid: { color:'rgba(31,41,55,0.8)' },
          ticks:{ color:'#9ca3af' }
        }
      }
    }
  });
}

async function loadEmployees(){
  const area = document.getElementById('employeesArea');
  area.innerHTML = 'Loading...';
  try {
    const list = await fetchJSON(API + '/employees');
    employeesData = list;
    renderEmployees(list);
    updateDashboard();
  } catch(err){
    area.innerHTML = `<div class="msg err" style="display:block">Error: ${err.message}</div>`;
  }
}

async function loadLeaves(){
  const area = document.getElementById('leavesArea');
  area.innerHTML = 'Loading...';
  try {
    const list = await fetchJSON(API + '/leave');
    leavesData = list;
    renderLeaves(list);
    updateDashboard();
    renderStatusChart(list);
  } catch(err){
    area.innerHTML = `<div class="msg err" style="display:block">Error: ${err.message}</div>`;
  }
}

// Add employee
document.getElementById('btnAdd').addEventListener('click', async ()=>{
  const name = document.getElementById('emp_name').value.trim();
  const balance = document.getElementById('emp_balance').value;
  if (!name) return showMsg(document.getElementById('addMsg'),'Name required',false);
  try {
    const res = await fetchJSON(API + '/employees', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({name, total_leave_balance: Number(balance)})
    });
    showMsg(document.getElementById('addMsg'),'Employee added: ID ' + res.employee_id, true);
    document.getElementById('emp_name').value = '';
    loadEmployees();
  } catch(e){
    showMsg(document.getElementById('addMsg'), e.message, false);
  }
});

// Refresh
document.getElementById('btnRefresh').addEventListener('click', ()=>{
  loadEmployees();
  loadLeaves();
});

// Apply leave
document.getElementById('btnApply').addEventListener('click', async ()=>{
  const emp = Number(document.getElementById('apply_emp').value);
  const type = document.getElementById('apply_type').value || 'Casual';
  const start = document.getElementById('apply_start').value;
  const end = document.getElementById('apply_end').value;
  if (!emp || !start || !end) return showMsg(document.getElementById('applyMsg'),'Fill all fields',false);
  try {
    const res = await fetchJSON(API + '/leave', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({employee_id: emp, leave_type: type, start_date: start, end_date: end})
    });
    showMsg(document.getElementById('applyMsg'),'Leave requested: ID ' + res.request_id, true);
    loadLeaves();
    loadEmployees();
  } catch(e){
    showMsg(document.getElementById('applyMsg'), e.message, false);
  }
});

// Summary
document.getElementById('btnSummary').addEventListener('click', async ()=>{
  const emp = Number(document.getElementById('sum_emp').value);
  const month = Number(document.getElementById('sum_month').value);
  const year = Number(document.getElementById('sum_year').value);
  const area = document.getElementById('summaryArea');
  area.innerHTML = 'Loading...';
  try {
    const data = await fetchJSON(`${API}/summary?employee_id=${emp}&month=${month}&year=${year}`);
    if (!data.length) { area.innerHTML = '<em>No records for this period</em>'; return; }
    let html = '<div style="overflow-x:auto;"><table><thead><tr><th>ID</th><th>Type</th><th>Days</th><th>Status</th><th>Applied On</th></tr></thead><tbody>';
    for (const r of data) {
      html += `<tr>
        <td>${r.request_id}</td>
        <td>${r.leave_type}</td>
        <td>${r.days}</td>
        <td>${statusBadge(r.status)}</td>
        <td>${r.applied_on}</td>
      </tr>`;
    }
    html += '</tbody></table></div>';
    area.innerHTML = html;
  } catch(e){
    area.innerHTML = `<div class="msg err" style="display:block">Error: ${e.message}</div>`;
  }
});

// Search: Employees
document.getElementById('searchEmp').addEventListener('input', function(){
  const q = this.value.toLowerCase();
  const filtered = employeesData.filter(e =>
    e.name.toLowerCase().includes(q) ||
    String(e.employee_id).includes(q)
  );
  renderEmployees(filtered);
});

// Search: Leaves
document.getElementById('searchLeave').addEventListener('input', function(){
  const q = this.value.toLowerCase();
  const filtered = leavesData.filter(r =>
    String(r.request_id).includes(q) ||
    String(r.employee_id).includes(q) ||
    (r.leave_type || '').toLowerCase().includes(q) ||
    (r.status || '').toLowerCase().includes(q)
  );
  renderLeaves(filtered);
  renderStatusChart(filtered.length ? filtered : leavesData);
});

// initial load
loadEmployees();
loadLeaves();
