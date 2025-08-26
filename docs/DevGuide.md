# Initial Code Setup
## UI
1. Creating a boilerplate nextjs app
```
(base) PS C:\code\chillpill\ui> npx create-next-app@latest chillpillui
√ Would you like to use TypeScript? ... No / Yes Yes
√ Would you like to use ESLint? ... No / Yes Yes
√ Would you like to use Tailwind CSS? ... No / Yes Yes
√ Would you like your code inside a `src/` directory? ... No / Yes Yes
√ Would you like to use App Router? (recommended) ... No / Yes Yes
√ Would you like to use Turbopack for `next dev`? ... No / Yes Yes
√ Would you like to customize the import alias (`@/*` by default)? ... No / Yes Yes
√ What import alias would you like configured? ... @/*
Creating a new Next.js app in C:\code\chillpill\ui\chillpillui.
```
2. Running the app
```
cd chillpillui
npm run dev
```
Visit http://localhost:3000 in your browser.


## Checking data in db
1. Install Mongosh
2. connect to cluster in powershell 
```
 mongosh "mongodb+srv://chillpillcluster.z3rolg2.mongodb.net/" --apiVersion 1 --username <Username>
```
3. Input the password when prompted
4. select the db
```
use chillpildb
```
5. Fetch collection data like below:
```
db.user.find() # Fetch all docs in user collection
db.users.find({ user_email: "someone@example.com" }) # Fetch docs from user collection based on the provided filter
```
