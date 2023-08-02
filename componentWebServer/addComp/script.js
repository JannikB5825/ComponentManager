const inputHandlerLcsc =  async function getCompInfoLcsc(e){
    const inputText = document.getElementById("lcsc-input").value;
    var cnumber;
    if(!inputText.startsWith("C")){
        cnumber = "C" + inputText;
    }
    else{
        cnumber = inputText;
    }
    const url = "/api/getComp";
    const data = {
        cNumber: cnumber,
    };

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    if(response.ok){
        const comp = await response.json();
        document.getElementById("comp-name").innerHTML = comp.name;
        document.getElementById("comp-catagory").innerHTML = comp.catagory;
        document.getElementById("comp-price").innerHTML = comp.price;
        document.getElementById("preview-img").src = comp.image;
        const table = document.getElementById("comp-parameter-table-lcsc")
        table.innerHTML = "";
        for(var parameter in comp.parameters){
            const row = document.createElement("tr");
            const para = document.createElement("td");
            para.textContent = comp.parameters[parameter][0];
            row.appendChild(para);
            const value = document.createElement("td");
            value.textContent = comp.parameters[parameter][1];
            row.appendChild(value);
            table.appendChild(row);
            //console.log(comp.parameters[parameter]);
        }
    }

}


const sourceLcsc = document.getElementById('lcsc-input');
sourceLcsc.addEventListener('input', inputHandlerLcsc);
sourceLcsc.addEventListener('propertychange', inputHandlerLcsc);
