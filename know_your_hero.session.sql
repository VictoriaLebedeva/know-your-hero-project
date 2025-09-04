SELECT * FROM users

SELECT * FROM refresh_token

SELECT * FROM users
WHERE email = 'ghost@company.com'

SELECT * FROM reviews

SELECT * from refresh_token
WHERE user_id = '665ff733-3583-4632-b518-e55bf9c68eed'
ORDER BY expires_at DESC


UPDATE users
SET role = 'guest'
WHERE id = '148af71a-db71-4b1b-af37-279024aafe08'