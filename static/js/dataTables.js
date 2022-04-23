document.addEventListener('DOMContentLoaded', function() {
    
    // CUSTOMER SCRIPT

    $('#employeeTable').DataTable( {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.11.3/i18n/pt_pt.json'
        },
        "columnDefs": [ { 
            "targets": [0,4],
            "orderable": false,
            "width": "16%"
        } ]
    } );
    $(".clickable-row, #employeeTable").click(function() {
        $(document).find('h4#form-modal-title').text("Editar Funcionário");
        $("#employeeModal").modal('show');
    });
    $("#addEmployeeButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar Funcionário");
    });
    $('#itemTable').DataTable( {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.11.3/i18n/pt_pt.json'
        },
        "columnDefs": [ { 
            "targets": [0,4],
            "orderable": false,
            "width": "16%"
        } ]
    } );
    $(".clickable-row, #itemTable").click(function() {
        $(document).find('h4#form-modal-title').text("Editar Item");
        $("#itemModal").modal('show');
    });
    $("#addItemButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar Item");
    });
    $(".clickable-row, #ivaTable").click(function () {
        $(document).find('h4#form-modal-title').text("Editar IVA");
        $("#addIvaModal").modal('show');
        //window.location = $(this).data("href");
    });
    $("#addIvaButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar IVA");
    });
    $('#positionTable').DataTable( {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.11.3/i18n/pt_pt.json'
        }
    } );
    $(".clickable-row, #positionTable").click(function() {
        $(document).find('h4#form-modal-title').text("Editar Cargo");
        $("#positionModal").modal('show');
    });
    $("#addPositionButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar Cargo");
    });
    $('#supplierTable').DataTable( {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.11.3/i18n/pt_pt.json'
        },
        "columnDefs": [ { 
            "targets": [0,4],
            "orderable": false,
            "width": "16%"
        } ]
    } );
    $(".clickable-row, #supplierTable").click(function() {
        $(document).find('h4#form-modal-title').text("Editar Fornecedor");
        $("#supplierModal").modal('show');
    });
    $("#addSupplierButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar Fornecedor");
    });
    $(".clickable-row, #titleTable").click(function () {
        $(document).find('h4#form-modal-title').text("Editar Título");
        $("#addTitleModal").modal('show');
        //window.location = $(this).data("href");
    });
    $("#addTitleButton").click(  function() {
        $(document).find('h4#form-modal-title').text("Adicionar Título");
    });
    
}); 



