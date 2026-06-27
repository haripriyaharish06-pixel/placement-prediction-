async function predict() {
    // 1. Grab all the actual values typed into your screen inputs
    const gender = document.getElementById('gender').value;
    const ssc_p = document.getElementById('ssc_p').value;
    const hsc_s = document.getElementById('hsc_s').value;
    const hsc_p = document.getElementById('hsc_p').value;
    const degree_t = document.getElementById('degree_t').value;
    const degree_p = document.getElementById('degree_p').value;
    const etest_p = document.getElementById('etest_p').value;

    // 2. Put them into a clean container to send over the network
    const formData = new FormData();
    formData.append('gender', gender);
    formData.append('ssc_p', parseFloat(ssc_p));
    formData.append('hsc_s', hsc_s);
    formData.append('hsc_p', parseFloat(hsc_p));
    formData.append('degree_t', degree_t);
    formData.append('degree_p', parseFloat(degree_p));
    formData.append('etest_p', parseFloat(etest_p));

    document.getElementById('result').innerText = "Calculating prediction...";

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
    method: 'POST',
    body: formData
});

        const result = await response.json();

        // 4. Print the final answer on your web screen
        if (result.prediction) {
            document.getElementById('result').innerText = "Prediction Result: " + result.prediction;
        } else if (result.error) {
            document.getElementById('result').innerText = "Server Error: " + result.error;
        }
    } catch (error) {
        console.error("Network Error:", error);
        document.getElementById('result').innerText = "Cannot reach server. Verify your terminal is running main.py!";
    }
}