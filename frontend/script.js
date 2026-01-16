const API_BASE_URL = "http://localhost:8000";

document.addEventListener('DOMContentLoaded', () => {
    // Customer Segmentation Logic
    const btnSegment = document.getElementById('btn-segment');
    const inputCustomer = document.getElementById('customer-id');
    const resultBoxSegment = document.getElementById('segment-result');
    const segmentValue = document.getElementById('segment-value');

    btnSegment.addEventListener('click', async () => {
        const customerId = inputCustomer.value.trim();
        if (!customerId) return;

        setLoading(btnSegment, true);
        resultBoxSegment.classList.add('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/customer/${customerId}`);
            if (!response.ok) {
                throw new Error(response.status === 404 ? 'Customer not found' : 'API Error');
            }
            const data = await response.json();

            segmentValue.textContent = data.segment;
            resultBoxSegment.classList.remove('hidden');
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(btnSegment, false);
        }
    });

    // Recommendation Logic
    const btnRecommend = document.getElementById('btn-recommend');
    const inputProduct = document.getElementById('product-name');
    const resultListRecommend = document.getElementById('recommend-result');

    btnRecommend.addEventListener('click', async () => {
        const productName = inputProduct.value.trim();
        if (!productName) return;

        setLoading(btnRecommend, true);
        resultListRecommend.innerHTML = '';
        resultListRecommend.classList.add('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/recommend/${encodeURIComponent(productName)}`);
            if (!response.ok) throw new Error('Failed to fetch recommendations');

            const data = await response.json();

            if (data.message) {
                resultListRecommend.innerHTML = `<div class="result-card"><span class="reco-name">${data.message}</span></div>`;
            } else {
                data.recommendations.forEach(rec => {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.innerHTML = `
                        <span class="reco-name">${rec.product}</span>
                        <span class="reco-score">Confidence (Lift): ${rec.confidence_score}</span>
                    `;
                    resultListRecommend.appendChild(card);
                });
            }
            resultListRecommend.classList.remove('hidden');
        } catch (error) {
            alert(error.message);
        } finally {
            setLoading(btnRecommend, false);
        }
    });

    function setLoading(button, isLoading) {
        if (isLoading) {
            button.dataset.originalText = button.textContent;
            button.textContent = 'Analyzing...';
            button.disabled = true;
            button.style.opacity = '0.7';
        } else {
            button.textContent = button.dataset.originalText;
            button.disabled = false;
            button.style.opacity = '1';
        }
    }
});
