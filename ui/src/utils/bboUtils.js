/**
 * Function to parse the BBO update JSON string.
 * @param {string} jsonString - The JSON string received from the server.
 * @returns {Object|null} - An object containing bestBid and bestAsk or null if an error occurs.
 */
export const parseBboUpdate = (jsonString) => {
    try {
        // Parse the JSON string
        const data = JSON.parse(jsonString);

        // Extract best_bid and best_ask
        const bestBid = data.best_bid;
        const bestAsk = data.best_ask;

        // Return parsed values
        return {
            bestBid,
            bestAsk,
        };
    } catch (error) {
        console.error("Error parsing BBO update:", error);
        return null; // Return null or handle the error as needed
    }
};