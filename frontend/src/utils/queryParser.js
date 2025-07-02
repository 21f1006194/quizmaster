// Query parser utility for advanced search functionality

export class QueryParser {
    constructor() {
        this.operators = {
            AND: 'AND',
            OR: 'OR',
            NOT: 'NOT'
        };
    }

    parse(query) {
        if (!query) return null;

        const tokens = this.tokenize(query);
        return this.buildQueryTree(tokens);
    }

    tokenize(query) {
        // Split by spaces but preserve quoted strings
        const tokens = [];
        let current = '';
        let inQuotes = false;

        for (let i = 0; i < query.length; i++) {
            const char = query[i];

            if (char === '"') {
                inQuotes = !inQuotes;
                continue;
            }

            if (char === ' ' && !inQuotes) {
                if (current) {
                    tokens.push(this.createToken(current));
                    current = '';
                }
                continue;
            }

            current += char;
        }

        if (current) {
            tokens.push(this.createToken(current));
        }

        return tokens;
    }

    createToken(value) {
        // Check for field-specific searches
        if (value.includes(':')) {
            const [field, ...rest] = value.split(':');
            const searchValue = rest.join(':');

            // Handle date filters
            if (field === 'after' || field === 'before') {
                return {
                    type: 'DATE_FILTER',
                    field,
                    value: searchValue
                };
            }

            // Handle duration filters
            if (field === 'duration') {
                return {
                    type: 'DURATION_FILTER',
                    value: this.parseDurationFilter(searchValue)
                };
            }

            // Handle field-specific searches
            return {
                type: 'FIELD_SEARCH',
                field,
                value: searchValue
            };
        }

        // Handle OR operator
        if (value === '|') {
            return {
                type: 'OPERATOR',
                value: this.operators.OR
            };
        }

        // Handle NOT operator
        if (value.startsWith('-')) {
            return {
                type: 'NOT',
                value: value.substring(1)
            };
        }

        // Handle quoted strings
        if (value.startsWith('"') && value.endsWith('"')) {
            return {
                type: 'EXACT_PHRASE',
                value: value.slice(1, -1)
            };
        }

        // Default to AND operator
        return {
            type: 'TERM',
            value
        };
    }

    parseDurationFilter(value) {
        if (value.includes('-')) {
            const [min, max] = value.split('-').map(Number);
            return { type: 'RANGE', min, max };
        }

        if (value.startsWith('>')) {
            return { type: 'GREATER_THAN', value: Number(value.substring(1)) };
        }

        if (value.startsWith('<')) {
            return { type: 'LESS_THAN', value: Number(value.substring(1)) };
        }

        return { type: 'EXACT', value: Number(value) };
    }

    buildQueryTree(tokens) {
        const query = {
            terms: [],
            filters: [],
            operators: []
        };

        let currentTerm = null;
        let currentOperator = this.operators.AND;

        for (const token of tokens) {
            if (token.type === 'OPERATOR') {
                currentOperator = token.value;
                query.operators.push(currentOperator);
                continue;
            }

            if (token.type === 'NOT') {
                currentTerm = {
                    type: 'NOT',
                    value: token.value
                };
            } else if (token.type === 'EXACT_PHRASE') {
                currentTerm = {
                    type: 'EXACT_PHRASE',
                    value: token.value
                };
            } else if (token.type === 'FIELD_SEARCH') {
                currentTerm = token;
            } else if (token.type === 'DATE_FILTER' || token.type === 'DURATION_FILTER') {
                query.filters.push(token);
                continue;
            } else {
                currentTerm = {
                    type: 'TERM',
                    value: token.value
                };
            }

            query.terms.push(currentTerm);
        }

        return query;
    }
} 