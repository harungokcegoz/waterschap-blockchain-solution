CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    reward_requested BOOLEAN NOT NULL DEFAULT FALSE,
    wallet_address VARCHAR(100)
);

INSERT INTO users (first_name, last_name, address, phone_number, email, wallet_address)
VALUES
    ('John', 'Doe', 'Lavaspad 352, 1032 VB Amsterdam, Netherlands', '1234567890', 'john@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae'),
    ('Jane', 'Smith', 'Marnixstraat 162, 1015 WB Amsterdam, Netherlands', '9876543210', 'jane@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae'),
    ('Alice', 'Johnson', 'John Hadleystraat 1887, 1086 WB Amsterdam, Netherlands', '5555555555', 'alice@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae'),
    ('Bob', 'Brown', 'Kees Broekmanstraat 176, 1095 MS Amsterdam, Netherlands', '1111111111', 'bob@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae'),
    ('Emma', 'Davis', 'Kees Broekmanstraat 240, 1095 MS Amsterdam, Netherlands', '2222222222', 'emma@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae'),
    ('Michael', 'Wilson', 'Nieuwezijds Voorburgwal 162, 1012 SJ Amsterdam, Netherlands', '3333333333', 'michael@example.com', '0x6cd79b86c6e98972b046c6fa0eaf39d91be461ae');

CREATE TABLE agents (
    agent_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    working_branch VARCHAR(100) NOT NULL,
    responsible_area VARCHAR(100) NOT NULL
);

INSERT INTO agents (first_name, last_name, email, hashed_password, working_branch, responsible_area)
VALUES
    ('Agent1', 'Smith', 'Aa&Maas@waterschap.com', '$2b$12$puuJFdkNjYGe2OPlUH8kWOo6s3fFmsc4/ahN04Zr4pSs5kbtQlH7W', 'Branch1', 'Area1'),
    ('Agent2', 'Johnson', 'johnson@example.com', '$2b$12$puuJFdkNjYGe2OPlUH8kWOo6s3fFmsc4/ahN04Zr4pSs5kbtQlH7W', 'Branch2', 'Area2'),
    ('Agent3', 'Williams', 'williams@example.com', '$2b$12$puuJFdkNjYGe2OPlUH8kWOo6s3fFmsc4/ahN04Zr4pSs5kbtQlH7W', 'Branch3', 'Area3');

CREATE TABLE user_requests
(
    request_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_address VARCHAR(255),
    approval_status VARCHAR(50), -- Status of the approval (pending, approved, rejected)
    rejection_reason VARCHAR(1000), -- Nullable column for rejection reason
    date_requested TIMESTAMP,
    installation_type VARCHAR(20), -- Assuming installation type can be either 'self' or 'technician'
    image_hashes TEXT[], -- Array of image hashes
    agent_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
    date_approved VARCHAR(255), -- Nullable column for approval date
    date_rejected VARCHAR(255) -- Nullable column for rejection date

);

INSERT INTO user_requests (user_id, user_address, approval_status, rejection_reason, installation_type, image_hashes, date_requested, agent_id, date_approved, date_rejected)
VALUES 
(
    1, -- User ID for the first user
    'Lavaspad 352, 1032 VB Amsterdam, Netherlands', -- Address for the first user
    'Pending', -- Set the initial status to 'Pending'
    NULL, -- Set the initial value of rejection_reason to null
    'Self', -- Assuming the user installed it themselves
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-04-04 12:00:00', -- Example date and time
    1, -- Agent ID 1
    NULL,
    NULL
),
(
    2, -- User ID for the second user
    'Marnixstraat 350, 1015 WB Amsterdam, Netherlands', -- Address for the second user
    'Pending', -- Set the initial status to 'Pending'
    NULL, -- Set the initial value of rejection_reason to null
    'Self', -- Assuming the user installed it themselves
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-04-10 14:00:00', -- Example date and time
    2, -- Agent ID 2
    NULL,
    NULL
),
(
    1, -- User ID
    'Lavaspad 352, 1032 VB Amsterdam, Netherlands',
    'Approved', -- Set the status to 'Approved'
    NULL, -- No rejection reason for approved requests
    'By Technician', -- Installed by a Technician
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-01 09:00:00', -- Example date and time
    1, -- Agent ID 1
    NULL,
    NULL
),
(
    2, -- User ID
    'Marnixstraat 350, 1015 WB Amsterdam, Netherlands',
    'Rejected', -- Set the status to 'Rejected'
    'Incomplete documentation', -- Reason for rejection
    'Self', -- Assuming the user installed it themselves
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-03 11:00:00', -- Example date and time
    2, -- Agent ID 2
    NULL,
    NULL
),
(
    3, -- User ID
    'John Hadleystraat 1887, 1086 WB Amsterdam, Netherlands',
    'Pending', -- Set the initial status to 'Pending'
    NULL, -- Set the initial value of rejection_reason to null
    'Self', -- Assuming the user installed it themselves
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-05 15:00:00', -- Example date and time
    1, -- Agent ID 1
    NULL,
    NULL
),
(
    4, -- User ID
    'Kees Broekmanstraat 176, 1095 MS Amsterdam, Netherlands',
    'Approved', -- Set the status to 'Approved'
    NULL, -- No rejection reason for approved requests
    'By Technician', -- Installed by a Technician
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-07 13:00:00', -- Example date and time
    2, -- Agent ID 2
    NULL,
    NULL
),
(
    5, -- User ID
    'Kees Broekmanstraat 240, 1095 MS Amsterdam, Netherlands',
    'Rejected', -- Set the status to 'Rejected'
    'Installation issues', -- Reason for rejection
    'Self', -- Assuming the user installed it themselves
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-09 10:00:00', -- Example date and time
    1, -- Agent ID 1
    NULL,
    NULL
),
(
    6, -- User ID
    'Nieuwezijds Voorburgwal 162, 1012 SJ Amsterdam, Netherlands',
    'Pending', -- Set the initial status to 'Pending'
    NULL, -- Set the initial value of rejection_reason to null
    'By Technician', -- Installed by a Technician
    ARRAY['bafybeifcp3x5nwjqc2mplcewjytd4pw44x5kxj5wrohvgjdbvfde3z4b6u', 'bafybeiailbqh5fvk6cag2gq2n2h3hgaadnfy7a36wnihywhlfhcxr6aoaa', 'bafkreiajhgpg64su2c7q7sab7xaztrlgzd3wqvjycjolyv5oqrjkb32mnu'], -- Array of image hashes
    '2024-05-11 16:00:00', -- Example date and time
    2, -- Agent ID 2
    NULL,
    NULL
);


CREATE TABLE measures
(
    measure_id SERIAL PRIMARY KEY,
    request_id INT NOT NULL,
    measure_type VARCHAR(100),
    measure_value VARCHAR(100),
    FOREIGN KEY (request_id) REFERENCES user_requests(request_id)
);

INSERT INTO measures (request_id, measure_type, measure_value)
VALUES (
    1, -- request_id associated with the measure
    'Rain Barrel', -- measure_type
    '100' -- measure_value
),
    (
    1, -- request_id associated with the measure
    'Rain Barrel', -- measure_type
    '150' -- measure_value
),
    (
    1, -- request_id associated with the measure
    'Rain Barrel', -- measure_type
    '200' -- measure_value
),
    (
    2, -- Request ID associated with the measure
    'Rain Barrel', -- Measure type
    '150' -- Measure value
),
    (
    2, -- Request ID associated with the measure
    'Rain Barrel', -- Measure type
    '150' -- Measure value
);