const searchField = document.getElementById('searchField');
const table_output = document.getElementById('outputtable');
const app_table = document.getElementById('apptable');
const paginationcontainer=document.getElementById('paginationcontainer');
const tbody=document.getElementById('outputtablebody');
table_output.style.display='none';




searchField.addEventListener('keyup', (e) => {

	const searchvalue=e.target.value;

	if (searchvalue.trim().length>0)
	{
        tbody.innerHTML='';
        paginationcontainer.style.display='none';

		fetch('/admin_search_billrecords',
			{
				method:"POST",



			body:JSON.stringify({searchText:searchvalue}),

		})

			.then((res) => res.json())
			.then((data)=>
			{
			    console.log('data',data);
                app_table.style.display='none';
                table_output.style.display='block';

                if(data.length===0)
                {
                    table_output.innerHTML='No record found';

                }
                else
                    {

                    data.forEach((item) =>
                        {
                        tbody.innerHTML+=
                            `<tr>
                                <td>${item.id}</td>
                                <td>${item.charge_date}</td>
                                <td>${item.doc_charges}</td>
                                <td>${item.doc_charges}</td>
                                <td>${item.medi_charges}</td>
                                <td>${item.room_charges}</td>
                                <td>${item.surgery_charges}</td>
                                <td>${item.admission_days}</td>
                                <td>${item.nursing_charges}</td>
                                <td>${item.advance}</td>
                                <td>${item.test_charges}</td>
                                <td>${item.bill_amount}</td>
                                <td>${item.pay_date}</td>
                                <td>${item.pay_amount}</td>
                                <td>${item.ins_copay}</td>
                                <td>${item.balance}</td>









                            </tr>`;

                        });
                }

			});
	}
	else {
	    table_output.style.display='none';
	    app_table.style.display='block';
	    paginationcontainer.style.display='block';
    }


});
