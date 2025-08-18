        const ragProgress = document.getElementById("ragProgress");
        const imageProgress = document.getElementById("imageProgress");
        const txtsqlProgress = document.getElementById("txtsqlProgress");
        const reportProgress = document.getElementById("reportProgress");
        let sessionId = sessionStorage.getItem('session_id');
        const BASE_URL = "http://3.109.213.80:8000";
        
        function generateUUID() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
            }

        if (!sessionId) {
            sessionId = generateUUID();
            sessionStorage.setItem('session_id', sessionId);
        }

        function clearControls(){
            document.getElementById("imageResponse").innerHTML = "";
            document.getElementById("ragResponse").innerHTML = "";
            document.getElementById("txtsqlResponse").innerHTML = "";
            document.getElementById("reportResponse").innerHTML = "";
            const textboxes = document.querySelectorAll('input[type="text"]');
            textboxes.forEach(input => input.value = "");
            document.getElementById("imageFile").value = "";

        }
        function toggleMode() {
            clearControls()
            const mode = document.getElementById("modeSelect").value;
            document.getElementById("ragMode").classList.add("hidden");
            document.getElementById("imageUploadMode").classList.add("hidden");
            document.getElementById("textSqlMode").classList.add("hidden");
            document.getElementById("reportMode").classList.add("hidden");

            if (mode === "RAG") document.getElementById("ragMode").classList.remove("hidden");
            if (mode === "Image-Upload") document.getElementById("imageUploadMode").classList.remove("hidden");
            if (mode === "Text-SQL") document.getElementById("textSqlMode").classList.remove("hidden");
            if (mode === "Generate Report") document.getElementById("reportMode").classList.remove("hidden");
        }

        document.getElementById("ragForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const question = document.getElementById("ragQuestion").value;
            const formData = new FormData();
            formData.append("question", question);
            ragProgress.classList.remove("d-none");

            const response = await fetch(`${BASE_URL}/rag-pdf`, {
                method: "POST",
                body: formData
            });
           
            const data = await response.json();
            ragProgress.classList.add("d-none");
            document.getElementById("ragResponse").innerHTML = `
            <div class='message question'>Question: ${question}</div>
            <div class='message answer'>Answer: ${data.answer || JSON.stringify(data)}</div>
            ` + document.getElementById("ragResponse").innerHTML;
        });

        document.getElementById("imageForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const file = document.getElementById("imageFile").files[0];
            const question = document.getElementById("imageQuestion").value;

            const formData = new FormData();
            formData.append("file", file);
            formData.append("question", question);
            imageProgress.classList.remove("d-none");

            const response = await fetch(`${BASE_URL}/extract-image`, {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            imageProgress.classList.add("d-none");
            document.getElementById("imageResponse").innerHTML = `
                <div class='message question'>Question: ${question}</div>
                <div class='message answer'>Answer: ${data.answer || JSON.stringify(data)}</div>
            `+ document.getElementById("imageResponse").innerHTML;
        });

        document.getElementById("txtsqlForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const question = document.getElementById("txtsqlquestion").value;
            const formData = new FormData();
            formData.append("question", question);
            formData.append("session_id", sessionId);
            txtsqlProgress.classList.remove("d-none");

            const response = await fetch(`${BASE_URL}/text-sql`, {
                method: "POST",
                body: formData
            });
           
            const data = await response.json();
            txtsqlProgress.classList.add("d-none");
            document.getElementById("txtsqlResponse").innerHTML = `
            <div class='message question'>Question: ${question}</div>
            <div class='message answer'>Answer: ${data.answer || JSON.stringify(data)}</div>
            ` + document.getElementById("txtsqlResponse").innerHTML;
        });

        document.getElementById("reportForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const question = document.getElementById("reportquestion").value;
            const formData = new FormData();
            formData.append("question", question);
            reportProgress.classList.remove("d-none");
          
            const response = await fetch(`${BASE_URL}/report`, {
                method: "POST",
                body: formData
            });
            const resultdata = await response.json();
            reportProgress.classList.add("d-none");
            const htmlUrl = resultdata.chat_history.find(
                            item => typeof item.content === "string" && item.content.includes(".html")
                            && item.name == "ReportGenerator")?.content;
                            let answerHtml = "";
                            if (htmlUrl) {
                                const filename = htmlUrl.split('/').pop() || "report.html";
                                answerHtml = `<button id="downloadReportBtn" class="download-btn">Download HTML Report</button>`;
                                 setTimeout(() => {
                                            document.getElementById("downloadReportBtn").addEventListener("click", async () => {
                                                const fileResponse = await fetch(htmlUrl);
                                                const blob = await fileResponse.blob();
                                                const url = window.URL.createObjectURL(blob);
                                                const a = document.createElement("a");
                                                a.href = url;
                                                a.download = filename;
                                                document.body.appendChild(a);
                                                a.click();
                                                document.body.removeChild(a);
                                                window.URL.revokeObjectURL(url);
                                            });
                                        }, 0);
                            } else {
                                answerHtml = `<span style="color:red;">No HTML report found</span>`;
                            }

             document.getElementById("reportResponse").innerHTML = `
            <div class='message question'>Question: ${question}</div>
            <div class='message answer'>Answer: ${answerHtml}</div>
            ` + document.getElementById("reportResponse").innerHTML;

        });

