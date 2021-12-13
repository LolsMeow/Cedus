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

		fetch('/search_vitals',
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
                                <td>${item.u_name}</td>
                                <td>${item.vt_date}</td>

                                <td>${item.vt_bloodgroup}</td>

                                <td>${item.vt_bp_sys}</td>
                                <td>${item.vt_bp_dia}</td>
                                <td>${item.vt_wbc}</td>
                                <td>${item.vt_rbc}</td>
                                <td>${item.vt_height}</td>
                                <td>${item.vt_weight}</td>
                                <td>${item.vt_comments}</td>
                                <td></td>



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
