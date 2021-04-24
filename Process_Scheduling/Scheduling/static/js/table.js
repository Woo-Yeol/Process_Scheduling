// 테이블 추가,삭제
localStorage.setItem("count", 6);
var full_count = 15;
var count = localStorage.count;

function addRow() {

    if (Number(localStorage.count) > full_count) {
        alert("최대15개까지만 가능합니다.");
        return;
    }

    var add_cell1 = "<b>" + Number(localStorage.count) + "</b>";
    var add_cell2 =
        '<input type="text" class="form-control" placeholder="Arrive Time" aria-label="Arrive Time" name="Arrive_time" >';
    var add_cell3 =
        '<input type="text" class="form-control" placeholder="Burst Time" aria-label="Burst Time" name="Burst_time">';
    var add_cell4 = "<label>-</label>";
    var add_cell5 = "<label>-</label>";
    var add_cell6 = "<label>-</label>";


    var table_name = document.getElementById("table");

    var new_row = table_name.insertRow();

    var new_cell1 = new_row.insertCell();
    var new_cell2 = new_row.insertCell();
    var new_cell3 = new_row.insertCell();
    var new_cell4 = new_row.insertCell();
    var new_cell5 = new_row.insertCell();
    var new_cell6 = new_row.insertCell();

    new_cell1.innerHTML = add_cell1;
    new_cell2.innerHTML = add_cell2;
    new_cell3.innerHTML = add_cell3;
    new_cell4.innerHTML = add_cell4;
    new_cell5.innerHTML = add_cell5;
    new_cell6.innerHTML = add_cell6;

    localStorage.count = Number(localStorage.count) + 1;
}

function deleteRow() {
    var table = document.getElementById("table");

    if (table.rows.length < 3) {
        alert("더이상 삭제할수 없습니다.");
        return;
    }

    table.deleteRow(table.rows.length - 1);
    localStorage.count = Number(localStorage.count) - 1;
}

// TimeQuantum 보이기 숨기기
function showTimeQuantum(e) {
    const type = e.options[e.selectedIndex].text;

    if (type.indexOf('RR') != 0) {
        document.getElementById('col-xs-2').style.visibility = "hidden";
    } else {
        document.getElementById('col-xs-2').style.visibility = "visible";
    }

}